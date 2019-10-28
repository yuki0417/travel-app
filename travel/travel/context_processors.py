from django.urls import reverse

from accounts.models import AppUser


def common(request, *args, **kwargs):
    """
    セッション情報を使ってユーザーの情報をテンプレートに表示する
    """
    # 対象外のURLかを判定
    if is_exclude_url(request) is True:
        return {}

    # セッションにユーザー情報がある場合
    if request.session.get('user_id', False):
        user_id = request.session.get('user_id', False)
        user = AppUser.objects.get(id=user_id)
    else:
        return {}

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
        'accounts:signup',
        'accounts:logged_out'
    ]
    for url in exclude_url:
        if request.path.startswith(reverse(url)):
            return True
    return False
