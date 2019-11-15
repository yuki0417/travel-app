from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse_lazy

from test.setting.selenium_setting import SELENIUM_SETTING
from test.unittest.common.test_data import (
    teardown_data,
    AppUserEncPasswordTestData1st,
    COR_APPUSER_DATA_1st,
)


class MySeleniumTests(StaticLiveServerTestCase):

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

    def test_signup__from_login_page(self):
        """
        ログイン画面にアクセスし、新規登録ボタンを押す
        =>新規登録の画面に遷移する
        """
        # ログイン画面にアクセス
        self.selenium.get(
            '%s%s' % (
                self.live_server_url,
                str(reverse_lazy('accounts:login'))))
        # 新規登録ボタンを押す
        self.selenium.find_element_by_xpath(
            '/html/body/div/div/div/div[2]/div/a').click()

        result = self.selenium.current_url
        expected = \
            self.live_server_url + str(reverse_lazy('accounts:signup'))

        self.assertEqual(result, expected)

    def test_signup__when_success(self):
        """
        新規登録画面にアクセスし、ユーザー登録を行う
        =>場所一覧の画面に遷移する
        """
        # 新規登録画面にアクセス
        self.selenium.get(
            '%s%s' % (
                self.live_server_url,
                str(reverse_lazy('accounts:signup'))))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys(COR_APPUSER_DATA_1st['username'])
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys(COR_APPUSER_DATA_1st['password'])
        password_input = self.selenium.find_element_by_name("password_check")
        password_input.send_keys(COR_APPUSER_DATA_1st['password'])
        self.selenium.find_element_by_xpath(
            '/html/body/div/div/div/form/div[4]/button').click()

        result = self.selenium.current_url
        expected = \
            self.live_server_url + str(reverse_lazy('travel:place_list'))

        self.assertEqual(result, expected)

    def test_signup__when_failed(self):
        """
        新規登録画面にアクセスし、すでに存在するユーザー登録を行う
        =>新規登録画面のままになる
        """
        # 同一のユーザーを登録しておく
        AppUserEncPasswordTestData1st.setUp()

        # 新規登録画面にアクセス
        self.selenium.get(
            '%s%s' % (
                self.live_server_url,
                str(reverse_lazy('accounts:signup'))))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys(COR_APPUSER_DATA_1st['username'])
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys(COR_APPUSER_DATA_1st['password'])
        password_input = self.selenium.find_element_by_name("password_check")
        password_input.send_keys(COR_APPUSER_DATA_1st['password'])
        self.selenium.find_element_by_xpath(
            '/html/body/div/div/div/form/div[4]/button').click()

        result = self.selenium.current_url
        expected = \
            self.live_server_url + str(reverse_lazy('accounts:signup'))

        self.assertEqual(result, expected)