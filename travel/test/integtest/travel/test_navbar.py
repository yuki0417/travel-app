from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse_lazy

from test.setting.selenium_setting import SELENIUM_SETTING
from test.unittest.common.test_data import (
    teardown_data,
    AppUserEncPasswordTestData1st,
)
from test.integtest.test_common import (
    open_hamb_menu,
    nav_bar
)


class NavBarTests(StaticLiveServerTestCase):

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

    def test_open_saved_place_page(self):
        """
        「テストユーザーでログイン」し、
        ナビゲーションバーの気になる場所リストのリンクを開く
        """
        open_hamb_menu(self)

        self.selenium.find_element_by_xpath(
            nav_bar["saved_place_list"]).click()
        expect = '{}{}'.format(
                self.live_server_url,
                str(reverse_lazy('travel:saved_place'))
            )
        result = self.selenium.current_url

        self.assertEqual(result, expect)

    def test_open_setting_create_page(self):
        """
        「テストユーザーでログイン」し、
        ナビゲーションバーの設定の新規作成のリンクを開く
        """
        open_hamb_menu(self)

        self.selenium.find_element_by_xpath(
            nav_bar["setting_change"]).click()
        self.selenium.find_element_by_xpath(
            nav_bar["setting_create"]).click()
        expect = '{}{}'.format(
                self.live_server_url,
                str(reverse_lazy('travel:create_setting'))
            )
        result = self.selenium.current_url

        self.assertEqual(result, expect)

    def test_open_setting_list_page(self):
        """
        「テストユーザーでログイン」し、
        ナビゲーションバーの設定の変更＆削除のリンクを開く
        """
        open_hamb_menu(self)

        sleep(2)
        self.selenium.find_element_by_xpath(
            nav_bar["setting_change"]).click()
        self.selenium.find_element_by_xpath(
            nav_bar["setting_edit"]).click()
        expect = '{}{}'.format(
                self.live_server_url,
                str(reverse_lazy('travel:setting_list'))
            )
        result = self.selenium.current_url

        self.assertEqual(result, expect)

    def test_open_shared_place_list_page(self):
        """
        「テストユーザーでログイン」し、
        ナビゲーションバーのおすすめの場所のリンクを開く
        """
        open_hamb_menu(self)

        self.selenium.find_element_by_xpath(
            nav_bar["shared_place"]).click()
        expect = '{}{}'.format(
                self.live_server_url,
                str(reverse_lazy('travel:shared_place_list'))
            )
        result = self.selenium.current_url

        self.assertEqual(result, expect)

    def test_open_logout_page(self):
        """
        「テストユーザーでログイン」し、
        ナビゲーションバーのログアウトのリンクを開く
        """
        open_hamb_menu(self)

        self.selenium.find_element_by_xpath(
            nav_bar["logout"]).click()
        expect = '{}{}'.format(
                self.live_server_url,
                str(reverse_lazy('accounts:logout_confirm'))
            )
        result = self.selenium.current_url

        self.assertEqual(result, expect)
