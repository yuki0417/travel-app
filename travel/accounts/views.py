from django.shortcuts import render, redirect
from django.views.generic import CreateView, View
from django.utils import timezone
from django.contrib.auth.hashers import (
    make_password,
    check_password
)

from .forms import SignUpForm, LoginForm
from .models import AppUser


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
