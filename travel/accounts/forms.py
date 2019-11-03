from django import forms
from django.contrib.auth.hashers import check_password
from django.utils import timezone

from .models import AppUser


class SignUpForm(forms.ModelForm):
    """
    サインアップ画面用のフォーム
    """
    class Meta:
        model = AppUser
        fields = ("username", "password")
        widgets = {
            'password': forms.PasswordInput,
        }
    password_check = forms.CharField(
        widget=forms.PasswordInput)

    def clean(self):
        super().clean()
        if self.cleaned_data.get('password', None):
            password = self.cleaned_data.get('password', None)
            password_check = self.cleaned_data.get('password_check', None)
            if password != password_check:
                self.add_error('password', 'パスワードが異なっています。')


class LoginForm(forms.Form):
    """
    ログイン画面用のフォーム
    """
    username = forms.CharField(
        label='ユーザー名',
        max_length=100)
    password = forms.CharField(
        widget=forms.PasswordInput)

    def clean(self):
        super().clean()
        id_pw_missmuch_msg = 'IDまたはパスワードが異なっています。'
        if self.cleaned_data.get('username', None):
            username = self.cleaned_data.get('username', None)
            password = self.cleaned_data.get('password', None)
            try:
                user = AppUser.objects.get(username=username)
                # パスワードを暗号化して比較
                pw_check_result = check_password(password, user.password)
                if pw_check_result is True:
                    user.last_login = timezone.now()
                    user.save()
                else:
                    self.add_error('username', id_pw_missmuch_msg)
            except AppUser.DoesNotExist:
                self.add_error('username', id_pw_missmuch_msg)
