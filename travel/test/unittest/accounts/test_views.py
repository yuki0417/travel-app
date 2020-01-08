import re
from unittest.mock import patch, MagicMock
from io import StringIO

from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest
from django.test import TestCase

from accounts.forms import SignUpForm, LoginForm
from accounts.views import (
    SignUpView,
    LoginView,
    logout_confirm,
    logged_out,
    test_login,
)
from accounts.models import AppUser
from test.unittest.common.test_data import (
    COR_APPUSER_DATA_1st,
    AppUserCorrectTestData1st,
)


# htmlの比較の際にcsrfトークンの部分を取り除く関数
def remove_csrf(html_code):
    csrf_regex = r'csrfmiddlewaretoken.*\n'
    return re.sub(csrf_regex, '', html_code)


# WSGIRequest利用の際に呼び出すセッションデータのモックを作成する関数
def mock_wsgi_session_context():
    SessionStore = MagicMock()
    SessionStore.return_value.get.return_value = \
        COR_APPUSER_DATA_1st['id']

    WSGIRequest.session = SessionStore()


class SignUpViewTestcase(TestCase):
    """
    アカウント作成の画面のテスト
    """
    databases = '__all__'

    def setUp(self):
        AppUserCorrectTestData1st.setUp()

    def test_class_variable__is_registered_correctly(self):
        suv = SignUpView()
        self.assertEqual(
            suv.template_name,
            'accounts/signup.html'
        )

    @patch('accounts.views.SignUpForm')
    def test_post__when_form_is_valid(self, mock_form):
        mock_form.return_value.is_valid.return_value = True
        mock_form.return_value.save.return_value = AppUser.objects.get(
            id=COR_APPUSER_DATA_1st['id'])

        def getitem(name):
            return COR_APPUSER_DATA_1st['password']
        mock_form.return_value.data = MagicMock()
        mock_form.return_value.data.__getitem__.side_effect = getitem

        suv = SignUpView()
        request = WSGIRequest({
            'REQUEST_METHOD': 'POST',
            'PATH_INFO': 'accounts:signup',
            'wsgi.input': StringIO()})
        mock_wsgi_session_context()

        expect = redirect('travel:place_list')
        result = suv.post(request)
        self.assertEqual(
            remove_csrf(result.content.decode('utf-8')),
            remove_csrf(expect.content.decode('utf-8'))
        )

    def test_post__when_form_is_not_valid(self):
        suv = SignUpView()
        request = WSGIRequest({
            'REQUEST_METHOD': 'POST',
            'PATH_INFO': 'accounts:signup',
            'wsgi.input': StringIO()})
        mock_wsgi_session_context()

        expect = render(
            request,
            'accounts/signup.html',
            {'form': SignUpForm(data=request.POST)}
        )
        result = suv.post(request)
        self.assertEqual(
            remove_csrf(result.content.decode('utf-8')),
            remove_csrf(expect.content.decode('utf-8'))
        )

    def test_get(self):
        suv = SignUpView()
        request = WSGIRequest({
            'REQUEST_METHOD': 'POST',
            'PATH_INFO': 'accounts:signup',
            'wsgi.input': StringIO()})
        mock_wsgi_session_context()

        expect = render(
            request,
            'accounts/signup.html',
            {'form': SignUpForm()}
        )
        result = suv.get(request)
        self.assertEqual(
            remove_csrf(result.content.decode('utf-8')),
            remove_csrf(expect.content.decode('utf-8'))
        )


class LoginViewTestcase(TestCase):
    """
    ログインの画面のテスト
    """
    databases = '__all__'

    def setUp(self):
        AppUserCorrectTestData1st.setUp()

    def test_class_variable__is_registered_correctly(self):
        lv = LoginView()
        self.assertEqual(
            lv.template_name,
            'accounts/login.html'
        )

    @patch('accounts.views.LoginForm')
    def test_post__when_form_is_valid(self, mock_form):
        mock_form.return_value.is_valid.return_value = True

        def getitem(name):
            return COR_APPUSER_DATA_1st['username']
        mock_form.return_value.data = MagicMock()
        mock_form.return_value.data.__getitem__.side_effect = getitem

        lv = LoginView()
        request = WSGIRequest({
            'REQUEST_METHOD': 'POST',
            'PATH_INFO': 'accounts:login',
            'wsgi.input': StringIO()})
        mock_wsgi_session_context()

        expect = redirect('travel:place_list')
        result = lv.post(request)
        self.assertEqual(
            remove_csrf(result.content.decode('utf-8')),
            remove_csrf(expect.content.decode('utf-8'))
        )

    def test_post__when_form_is_not_valid(self):
        lv = LoginView()
        request = WSGIRequest({
            'REQUEST_METHOD': 'POST',
            'PATH_INFO': 'accounts:login',
            'wsgi.input': StringIO()})
        mock_wsgi_session_context()

        expect = render(
            request,
            'accounts/login.html',
            {'form': LoginForm(data=request.POST)}
        )
        result = lv.post(request)
        self.assertEqual(
            remove_csrf(result.content.decode('utf-8')),
            remove_csrf(expect.content.decode('utf-8'))
        )

    def test_get(self):
        lv = LoginView()
        request = WSGIRequest({
            'REQUEST_METHOD': 'POST',
            'PATH_INFO': 'accounts:login',
            'wsgi.input': StringIO()})
        mock_wsgi_session_context()

        expect = render(
            request,
            'accounts/login.html',
            {'form': LoginForm()}
        )
        result = lv.get(request)
        self.assertEqual(
            remove_csrf(result.content.decode('utf-8')),
            remove_csrf(expect.content.decode('utf-8'))
        )


class LogOutTestcase(TestCase):
    """
    ログアウトの画面のテスト
    """
    databases = '__all__'

    def setUp(self):
        AppUserCorrectTestData1st.setUp()

    def test_logged_out(self):
        request = WSGIRequest({
            'REQUEST_METHOD': 'POST',
            'PATH_INFO': 'accounts:logout',
            'wsgi.input': StringIO()})
        mock_wsgi_session_context()
        result = logged_out(request)
        expect = render(request, 'accounts/logged_out.html')
        self.assertEqual(
            remove_csrf(result.content.decode('utf-8')),
            remove_csrf(expect.content.decode('utf-8'))
        )


class LogOutConfirmTestcase(TestCase):
    """
    ログアウトの画面のテスト
    """
    databases = '__all__'

    def setUp(self):
        AppUserCorrectTestData1st.setUp()

    def test_logout_confirm__when_post(self):
        request = WSGIRequest({
            'REQUEST_METHOD': 'POST',
            'PATH_INFO': 'accounts:logout_confirm',
            'wsgi.input': StringIO()})
        mock_wsgi_session_context()
        result = logout_confirm(request)
        expect = render(request, 'accounts/logged_out.html')
        self.assertEqual(
            remove_csrf(result.content.decode('utf-8')),
            remove_csrf(expect.content.decode('utf-8'))
        )

    def test_logout_confirm__when_not_post(self):
        request = WSGIRequest({
            'REQUEST_METHOD': 'GET',
            'PATH_INFO': 'accounts:logout_confirm',
            'wsgi.input': StringIO()})
        mock_wsgi_session_context()
        result = logout_confirm(request)
        expect = render(request, 'accounts/logout_confirm.html')
        self.assertEqual(
            remove_csrf(result.content.decode('utf-8')),
            remove_csrf(expect.content.decode('utf-8'))
        )


class TestLoginTestcase(TestCase):
    """
    ログアウトの画面のテスト
    """
    databases = '__all__'

    def setUp(self):
        AppUserCorrectTestData1st.setUp()

    @patch(
        'accounts.create_testuser.is_test_user_exists',
        MagicMock(return_value=False))
    @patch('accounts.create_testuser.create_test_user')
    def test_login__when_test_user_not_exists(self, mock_create_test_user):
        request = WSGIRequest({
            'REQUEST_METHOD': 'GET',
            'wsgi.input': StringIO()})
        mock_wsgi_session_context()

        mock_create_test_user.return_value = AppUser.objects.get(
            id=COR_APPUSER_DATA_1st['id'])
        expect = redirect('travel:place_list')
        result = test_login(request)
        self.assertEqual(
            remove_csrf(result.content.decode('utf-8')),
            remove_csrf(expect.content.decode('utf-8'))
        )

    @patch(
        'accounts.create_testuser.is_test_user_exists',
        MagicMock(return_value=True))
    @patch(
        'accounts.views.TEST_USER_INFO',
        MagicMock(return_value=COR_APPUSER_DATA_1st))
    def test_login__when_test_user_exists(self):
        request = WSGIRequest({
            'REQUEST_METHOD': 'GET',
            'wsgi.input': StringIO()})
        mock_wsgi_session_context()

        expect = redirect('travel:place_list')
        result = test_login(request)
        self.assertEqual(
            remove_csrf(result.content.decode('utf-8')),
            remove_csrf(expect.content.decode('utf-8'))
        )
