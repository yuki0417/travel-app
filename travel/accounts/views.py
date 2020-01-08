from django.shortcuts import render, redirect
from django.views.generic import CreateView, View
from django.utils import timezone
from django.contrib.auth.hashers import make_password

from .forms import SignUpForm, LoginForm
from .models import AppUser
from .create_testuser import (
    TEST_USER_INFO,
    create_test_user,
    is_test_user_exists,
)


class SignUpView(CreateView):
    """
    アカウント作成の画面
    """
    template_name = 'accounts/signup.html'

    def post(self, request, *args, **kwargs):
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            # フォームのデータを変数に保存する
            user = form.save(commit=False)
            # パスワードをハッシュ化して保存する
            user.password = make_password(form.data['password'])
            user.save()
            # userのセッションを保持する
            request.session['user_id'] = user.id
            return redirect('travel:place_list')
        else:
            return render(request, self.template_name, {'form': form})

    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        return render(request, self.template_name, {'form': form})


class LoginView(View):
    """
    ログインの画面
    """
    template_name = 'accounts/login.html'

    def post(self, request, *arg, **kwargs):
        form = LoginForm(data=request.POST)

        if form.is_valid():
            username = form.data['username']
            user = AppUser.objects.get(username=username)
            request.session['user_id'] = user.id
            return redirect('travel:place_list')
        else:
            return render(request, self.template_name, {'form': form})

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})


def logout_confirm(request):
    """
    ログアウト確認画面
    """
    if request.method == "POST":
        request.session.clear()
        return render(request, 'accounts/logged_out.html')
    else:
        return render(request, 'accounts/logout_confirm.html')


def logged_out(request):
    """
    ログアウト画面
    """
    return render(request, 'accounts/logged_out.html')


def test_login(request):
    """
    テストログイン処理
    """
    # ユーザーがない場合はテストユーザーを作成
    if is_test_user_exists() is False:
        user = create_test_user()
        user_id = user.id
    else:
        user = AppUser.objects.get(
            username=TEST_USER_INFO["username"])
        user_id = user.id
    # セッション情報、ログイン日時を保存
    request.session['user_id'] = user_id
    user.last_login = timezone.now()
    user.save()

    # 場所を探すページに遷移
    return redirect('travel:place_list')
