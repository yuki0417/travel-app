from django.test import TestCase
from django import forms

from accounts.models import AppUser
from accounts.forms import SignUpForm, LoginForm
from test.unittest.common.test_data import (
    COR_APPUSER_DATA_1st,
    AppUserCorrectTestData1st,
)


class MockSignUpForm(SignUpForm):
    """
    サインアップフォームのcleaned_dataの値を事前に用意しておく
    """
    cleaned_data = {
        'password': COR_APPUSER_DATA_1st['password'],
        'password_check': COR_APPUSER_DATA_1st['password'],
    }


class SignUpFormTestcase(TestCase):
    """
    サインアップ画面用のフォームのテスト
    """
    databases = '__all__'

    def setUp(self):
        AppUserCorrectTestData1st.setUp()

    def test_class_meta_variable__is_registered_correctly(self):
        meta = SignUpForm(AppUser).Meta()
        fields = ('username', 'password')
        self.assertEqual(meta.model, AppUser)
        self.assertEqual(meta.fields, fields)
        self.assertIsInstance(meta.widgets['password'], forms.PasswordInput)

    def test_class_variable__is_registered_correctly(self):
        suf = SignUpForm(AppUser)
        self.assertIsInstance(
            suf.fields.get('password_check').widget,
            forms.PasswordInput)

    def test_clean__password_has_no_error(self):
        msf = MockSignUpForm(instance=AppUser)
        msf.clean()
        result = msf.errors
        self.assertEqual(result, {})

    def test_clean__password_has_error(self):
        msf = MockSignUpForm(instance=AppUser)
        msf.cleaned_data['password_check'] = 'any_diiferent_pw'
        msf.clean()
        result = msf.errors['password'][0]
        expect = 'パスワードが異なっています。'
        self.assertEqual(result, expect)


class MockLoginForm(LoginForm):
    """
    ログイン画面用のフォームのcleaned_dataの値を事前に用意しておく
    """
    cleaned_data = {
        'username': COR_APPUSER_DATA_1st['username'],
        'password': COR_APPUSER_DATA_1st['password'],
    }


class LoginFormTestcase(TestCase):
    """
    ログイン画面用のフォームのテスト
    """
    databases = '__all__'

    def setUp(self):
        AppUserCorrectTestData1st.setUp()

    def test_class_meta_variable__is_registered_correctly(self):
        lf = LoginForm(AppUser)
        self.assertIsInstance(lf.fields['username'], forms.CharField)
        self.assertEqual(lf.fields['username'].label, 'ユーザー名')
        self.assertEqual(lf.fields['username'].max_length, 100)
        self.assertIsInstance(
            lf.fields['password'].widget,
            forms.PasswordInput)

    def test_clean__password_has_no_error(self):
        msf = MockLoginForm()
        msf.clean()
        result = msf.errors
        self.assertEqual(result, {})

    def test_clean__password_has_error_when_pw_different(self):
        msf = MockLoginForm()
        msf.cleaned_data['password'] = 'any_diiferent_pw'
        msf.clean()
        result = msf.errors['username'][0]
        expect = 'IDまたはパスワードが異なっています。'
        self.assertEqual(result, expect)

    def test_clean__password_has_error_when_user_not_exist(self):
        msf = MockLoginForm()
        msf.cleaned_data['username'] = 'any_not_exist_use'
        msf.clean()
        result = msf.errors['username'][0]
        expect = 'IDまたはパスワードが異なっています。'
        self.assertEqual(result, expect)
