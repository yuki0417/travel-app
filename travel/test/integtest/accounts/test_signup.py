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
from test.integtest.test_common import (
    signup_form,
    open_signup_page
)


class SignupTests(StaticLiveServerTestCase):

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

    def test_signup__when_success(self):
        """
        新規登録画面にアクセスし、ユーザー登録を行う
        =>場所一覧の画面に遷移する
        """
        # 新規登録画面にアクセス
        open_signup_page(self)

        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys(COR_APPUSER_DATA_1st['username'])
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys(COR_APPUSER_DATA_1st['password'])
        password_input = self.selenium.find_element_by_name("password_check")
        password_input.send_keys(COR_APPUSER_DATA_1st['password'])
        self.selenium.find_element_by_xpath(
            signup_form["register_btn"]).click()

        result = self.selenium.current_url
        expected = '{}{}'.format(
            self.live_server_url,
            str(reverse_lazy('travel:place_list'))
        )

        self.assertEqual(result, expected)

    def test_signup__when_failed(self):
        """
        新規登録画面にアクセスし、すでに存在するユーザー登録を行う
        =>新規登録画面のままになる
        """
        # 同一のユーザーを登録しておく
        AppUserEncPasswordTestData1st.setUp()

        # 新規登録画面にアクセス
        open_signup_page(self)

        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys(COR_APPUSER_DATA_1st['username'])
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys(COR_APPUSER_DATA_1st['password'])
        password_input = self.selenium.find_element_by_name("password_check")
        password_input.send_keys(COR_APPUSER_DATA_1st['password'])
        self.selenium.find_element_by_xpath(
            signup_form["register_btn"]).click()

        result = self.selenium.current_url
        expected = '{}{}'.format(
            self.live_server_url,
            str(reverse_lazy('accounts:signup'))
        )

        self.assertEqual(result, expected)
