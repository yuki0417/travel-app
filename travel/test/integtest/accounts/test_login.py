from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse_lazy

from test.setting.selenium_setting import SELENIUM_SETTING
from test.unittest.common.test_data import (
    teardown_data,
    AppUserEncPasswordTestData1st,
    COR_APPUSER_DATA_1st,
    COR_APPUSER_DATA_2nd,
)
from test.integtest.test_common import (
    login_form
)


class LoginTests(StaticLiveServerTestCase):

    def setUp(self):
        AppUserEncPasswordTestData1st.setUp()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chromedriver_path = SELENIUM_SETTING['chromedriver_path']
        o = Options()
        o.binary_location = SELENIUM_SETTING['binary_location']
        o.add_argument(SELENIUM_SETTING['headless'])
        o.add_argument(SELENIUM_SETTING['disable-gpu'])
        o.add_argument(SELENIUM_SETTING['no-sandbox'])
        o.add_argument(SELENIUM_SETTING['window-size'])
        cls.selenium = webdriver.Chrome(chromedriver_path, options=o)
        cls.selenium.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        teardown_data()
        cls.selenium.quit()
        super().tearDownClass()

    def login_with_test_user(self):
        self.selenium.get(
            '%s%s' % (
                self.live_server_url,
                str(reverse_lazy('accounts:login'))))
        self.selenium.find_element_by_xpath(
            login_form["test_login_btn"]).click()

    def test_login__when_success(self):
        """
        ログイン画面にアクセスし、必要なフォーム入力し、ログインボタンを押す
        =>場所一覧の画面に遷移する
        """
        # ログイン
        self.selenium.get(
            '%s%s' % (
                self.live_server_url,
                str(reverse_lazy('accounts:login'))))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys(COR_APPUSER_DATA_1st['username'])
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys(COR_APPUSER_DATA_1st['password'])
        self.selenium.find_element_by_xpath(
            login_form["login_btn"]).click()

        result = self.selenium.current_url
        expected = \
            self.live_server_url + str(reverse_lazy('travel:place_list'))

        self.assertEqual(result, expected)

    def test_login__when_failed(self):
        """
        ログイン画面にアクセスし、誤ったパスワードを入力し、ログインボタンを押す
        =>ログイン画面に遷移する
        """
        # ログイン
        self.selenium.get(
            '%s%s' % (
                self.live_server_url,
                str(reverse_lazy('accounts:login'))))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys(COR_APPUSER_DATA_1st['username'])
        password_input = self.selenium.find_element_by_name("password")
        # 誤ったパスワードを入力
        password_input.send_keys(COR_APPUSER_DATA_2nd['password'])
        self.selenium.find_element_by_xpath(
            login_form["login_btn"]).click()

        result = self.selenium.current_url
        expected = self.live_server_url + str(reverse_lazy('accounts:login'))

        self.assertEqual(result, expected)

    def test_login__when_test_user(self):
        """
        ログイン画面にアクセスし、「テストユーザーでログイン」ボタンを押す
        =>場所一覧の画面に遷移する
        """
        # テストユーザーログイン
        self.login_with_test_user()

        result = self.selenium.current_url
        expected = \
            self.live_server_url + str(reverse_lazy('travel:place_list'))

        self.assertEqual(result, expected)

    def test_login__go_to_signup_form(self):
        """
        ログイン画面にアクセスし、新規登録ボタンを押す
        =>新規登録の画面に遷移する
        """
        # ログイン画面
        self.selenium.get(
            '%s%s' % (
                self.live_server_url,
                str(reverse_lazy('accounts:login'))))
        # 新規登録するボタンを押す
        self.selenium.find_element_by_xpath(
            login_form["signup_btn"]).click()

        result = self.selenium.current_url
        expected = \
            self.live_server_url + str(reverse_lazy('accounts:signup'))

        self.assertEqual(result, expected)
