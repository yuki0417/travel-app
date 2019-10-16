from django.shortcuts import render, redirect
from django.views.generic import CreateView, View
from django.utils import timezone
from django.contrib.auth.hashers import (
    make_password,
    check_password
)

from .forms import SignUpForm, LoginForm
from .models import AppUser
from .create_testuser import (
    TEST_USER_INFO,
    create_test_user,
    test_user_exists,
)


class SignUpView(CreateView):
    """
    アカウント作成の画面
    """
    template_name = 'accounts/signup.html'

    def post(self, request, *args, **kwargs):
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            if form.data['password'] == form.data['password_check']:
                # フォームのデータを変数に保存する
                user = form.save(commit=False)
                # パスワードをハッシュ化して保存する
                user.password = make_password(form.data['password'])
                user.save()
                # userのセッションを保持する
                request.session['user_id'] = user.id
                return redirect('/travel/list')
            else:
                errors_message = True
                d = {
                    'form': form,
                    'errors_message': errors_message
                }
                return render(request, 'accounts/signup.html', d)
        else:
            return render(request, 'accounts/signup.html', {'form': form})

    def get(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        return render(request, 'accounts/signup.html', {'form': form})


class AccountLoginView(View):
    """
    ログインの画面
    """
    template_name = 'accounts/login.html'

    def post(self, request, *arg, **kwargs):
        form = LoginForm(data=request.POST)
        error_page = 'accounts/login.html'
        errors = {
            'form': form,
            'errors_message': True
        }

        if form.is_valid():
            username = form.data['username']
            try:
                user = AppUser.objects.get(
                    username=username)
            except AppUser.DoesNotExist:
                return render(request, error_page, errors)

            pw_check_result = check_password(
                form.data['password'], user.password)
            if pw_check_result is True:
                user.last_login = timezone.now()
                user.save()
                # userのセッションを保持する
                request.session['user_id'] = user.id
                return redirect('/travel/list')
            else:
                return render(request, error_page, errors)

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        return render(request, 'accounts/login.html', {'form': form})


def logout_confirm(request):
    if request.method == "POST":
        request.session.clear()
        return render(request, 'accounts/logged_out.html')
    else:
        return render(request, 'accounts/logout_confirm.html')


def logged_out(request):
    return render(request, 'accounts/logged_out.html')


def test_login(request):
    # ユーザーがない場合はテストユーザーを作成
    if test_user_exists() is False:
        test_user = create_test_user()
        user_id = test_user.id
    else:
        user = AppUser.objects.get(
            username=TEST_USER_INFO["username"])
        user_id = user.id
    # セッション情報、ログイン日時を保存
    request.session['user_id'] = user_id
    user.last_login = timezone.now()
    user.save()

    # 場所を探すページに遷移
    return redirect('/travel/list')
