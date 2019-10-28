from unittest.mock import patch, MagicMock, Mock
from io import StringIO

from django.urls import reverse
from django.core.handlers.wsgi import WSGIRequest
from django.test import TestCase

from travel.context_processors import (
    common,
    is_exclude_url
)
from test.unittest.common.test_data import (
    COR_APPUSER_DATA_1st,
    AppUserCorrectTestData1st,
)


context_1st = {
    'user_id': COR_APPUSER_DATA_1st['id'],
    'username': COR_APPUSER_DATA_1st['username'],
    'last_login': COR_APPUSER_DATA_1st['last_login'],
}


# WSGIRequest利用の際に呼び出すセッションデータのモックを作成する関数
def mock_wsgi_session_context():
    SessionStore = Mock()
    SessionStore.return_value.get.return_value = \
        COR_APPUSER_DATA_1st['id']
    WSGIRequest.session = SessionStore()


# WSGIRequest利用の際に呼び出すセッションデータのモックを作成する関数
def mock_wsgi_session_no_context():
    SessionStore = Mock()
    SessionStore.return_value.get.return_value = None
    WSGIRequest.session = SessionStore()


class CommonTestcase(TestCase):
    """
    common関数のテストケース
    """
    databases = '__all__'

    def setUp(self):
        AppUserCorrectTestData1st.setUp()

    @patch(
        'travel.context_processors.is_exclude_url',
        MagicMock(return_value=False))
    def test_coomon__with_no_exclude_url_and_session_exists(self):
        mock_wsgi_session_context()
        request = WSGIRequest({
            'REQUEST_METHOD': 'GET',
            'wsgi.input': StringIO()})

        result = common(request)
        self.assertEqual(result, context_1st)

    @patch(
        'travel.context_processors.is_exclude_url',
        MagicMock(return_value=False))
    def test_coomon__with_no_exclude_url_and_session_no_exists(self):
        mock_wsgi_session_no_context()
        request = WSGIRequest({
            'REQUEST_METHOD': 'GET',
            'wsgi.input': StringIO()})

        result = common(request)
        self.assertEqual(result, {})

    @patch(
        'travel.context_processors.is_exclude_url',
        MagicMock(return_value=True))
    def test_coomon__with_exclude_url(self):
        request = WSGIRequest({
            'REQUEST_METHOD': 'GET',
            'wsgi.input': StringIO()})

        result = common(request)
        self.assertEqual(result, {})


class IsExcludeUrlTestcase(TestCase):
    """
    is_exclude_url関数のテストケース
    """
    def test_is_exclude_url__url_exists(self):
        exclude_url = [
            'admin:index',
            'accounts:login',
            'accounts:signup',
            'accounts:logged_out'
        ]
        for url in exclude_url:
            request = WSGIRequest({
                'REQUEST_METHOD': 'GET',
                'PATH_INFO': reverse(url),
                'wsgi.input': StringIO()})
            result = is_exclude_url(request)
            self.assertEqual(result, True)

    def test_is_exclude_url__url_not_exists(self):
        not_exclude_url = [
            'travel:setting_list',
            'travel:place_list',
        ]
        for url in not_exclude_url:
            request = WSGIRequest({
                'REQUEST_METHOD': 'GET',
                'PATH_INFO': reverse(url),
                'wsgi.input': StringIO()})
            result = is_exclude_url(request)
            self.assertEqual(result, False)
