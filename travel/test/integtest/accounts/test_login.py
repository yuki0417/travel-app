from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse_lazy

from test.unittest.common.test_data import (
    teardown_data,
    AppUserEncPasswordTestData1st,
    COR_APPUSER_DATA_1st,
    COR_APPUSER_DATA_2nd,
)


class MySeleniumTests(StaticLiveServerTestCase):

    def setUp(self):
        AppUserEncPasswordTestData1st.setUp()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chromedriver_path = '/usr/bin/chromedriver'
        o = Options()
        o.binary_location = '/usr/bin/chromium'
        o.add_argument('--headless')
        o.add_argument('--disable-gpu')
        o.add_argument('--no-sandbox')
        o.add_argument('--window-size=1200x600')
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
            '/html/body/div/div/div/div[1]/div/a').click()

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
            '/html/body/div/div/div/form/div[3]/button').click()

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
            '/html/body/div/div/div/form/div[3]/button').click()

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
