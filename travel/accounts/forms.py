# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django import forms
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


class LoginForm(forms.Form):
    """
    ログイン画面用のフォーム
    """
    username = forms.CharField(
        label='ユーザー名',
        max_length=100)
    password = forms.CharField(
        widget=forms.PasswordInput)
