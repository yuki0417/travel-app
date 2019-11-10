from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse_lazy

from accounts.models import AppUser
from accounts.create_testuser import TEST_USER_INFO
from travel.models import Setting, Place
from test.unittest.common.test_data import (
    teardown_data,
    AppUserEncPasswordTestData1st,
    SettingCorrectTestData2ndUser1st,
    COR_APPUSER_DATA_1st,
    COR_APPUSER_DATA_2nd,
    COR_SETTING_DATA_1st,
    COR_SETTING_DATA_2nd,
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

    def test_create_setting__success(self):
        """
        「テストユーザーでログイン」し、場所を検索し、気になるリスト追加と取り消しを行う
        =>気になるリストに場所を追加、または取り消しができる
        """
        # テストユーザーログイン
        self.login_with_test_user()

        # 設定2のuserをユニットテストユーザーからテストユーザーに変更しておく
        SettingCorrectTestData2ndUser1st.setUp()
        test_setting_2nd = Setting.objects.get(id=COR_SETTING_DATA_2nd["id"])
        test_setting_2nd.user = \
            AppUser.objects.get(username=TEST_USER_INFO['username'])
        test_setting_2nd.save()

        # 設定表示のためページ読み直し
        self.selenium.refresh()

        # 位置情報の戻り値を固定させる
        self.selenium.execute_script(
            "window.navigator.geolocation.getCurrentPosition="
            "function(success){"
            "var position = "
            "{\"coords\" : {"
            "\"latitude\": \"35.55555\",\"longitude\": \"139.55555\"}};"
            "success(position);}")

        # 設定２を洗濯し、周辺のスポットをさがすボタンを押す
        select_setting = Select(
            self.selenium.find_element_by_name("setting_now"))
        select_setting.select_by_index(1)

        self.selenium.find_element_by_xpath(
            '/html/body/div[2]/form/button').click()

        # wikipediaAPI待機のため１０秒待つ
        sleep(10)

        # htmlのテーブルのパス
        place_table = (
            '/html/body/div[2]/div[2]/div[3]/div/div[2]/div/table/tbody/'
        )

        # 上から１つめと２つめのタイトルを変数に入れておく
        place_1_title = self.selenium.find_element_by_xpath(
            place_table + 'tr[1]/td[1]/h3').text
        place_2_title = self.selenium.find_element_by_xpath(
            place_table + 'tr[2]/td[1]/h3').text

        # それぞれ気になるリストに追加するボタンを押す
        self.selenium.find_element_by_xpath(
            place_table + 'tr[1]/td[1]/button').click()
        self.selenium.find_element_by_xpath(
            place_table + 'tr[2]/td[1]/button').click()

        # import pdb;pdb.set_trace()

        # 気になるリスト追加処理のため3秒待つ
        sleep(3)

        # 気になるリストに追加されている
        self.assertTrue(
            Place.objects.get(name=place_1_title)
        )
        self.assertTrue(
            Place.objects.get(name=place_2_title)
        )

        # それぞれ気になるリストから取り消すボタンを押す
        self.selenium.find_element_by_xpath(
            place_table + 'tr[1]/td[1]/button').click()
        self.selenium.find_element_by_xpath(
            place_table + 'tr[2]/td[1]/button').click()

        # 気になるリスト削除処理のため3秒待つ
        sleep(3)

        # 気になるリストから削除されている
        with self.assertRaises(Place.DoesNotExist):
            Place.objects.get(name=place_1_title)

        with self.assertRaises(Place.DoesNotExist):
            Place.objects.get(name=place_2_title)
