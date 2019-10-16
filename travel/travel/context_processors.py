from django.urls import reverse

from accounts.models import AppUser


TEST_USER_INFO = {
    "username": "テストユーザー",
    "password": "test",
}


def common(request, *args, **kwargs):
    """
    セッション情報を使ってユーザーの情報をテンプレートに表示する
    """
    # 対象外のURLかを判定
    if is_exclude_url(request) is True:
        return {}
    # ユーザーがない場合はテストユーザーを作成する
    if test_user_exists() is False:
        test_user = create_test_user()
        user_id = test_user.id

    # セッションにユーザー情報がある場合
    if request.session.get('user_id', False):
        user_id = request.session.get('user_id', False)
        user = AppUser.objects.get(id=user_id)
    # ユーザー情報がセッションにない場合は、テストユーザーのセッション情報の保存を行う
    else:
        user = AppUser.objects.get(username=TEST_USER_INFO["username"])
        request.session['user_id'] = user.id
        user_id = user.id

    context = {
        'user_id': user_id,
        'username': user.username,
        'last_login': user.last_login,
    }
    return context


def is_exclude_url(request):
    """
    下記のURLではsession情報を必要としないようにする
    """
    exclude_url = [
        'admin:index',
        'accounts:login',
        'accounts:signup'
    ]
    for url in exclude_url:
        if request.path.startswith(reverse(url)):
            return True


def create_test_user():
    user = AppUser.objects.create(
        username=TEST_USER_INFO["username"],
        password=TEST_USER_INFO["password"],
    )
    return user


def test_user_exists():
    try:
        AppUser.objects.get(
            username=TEST_USER_INFO["username"]
        )
    except AppUser.DoesNotExist:
        return False

    return True
