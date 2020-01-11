from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse_lazy

from test.setting.selenium_setting import SELENIUM_SETTING
from accounts.models import AppUser
from accounts.create_testuser import TEST_USER_INFO
from travel.models import Setting, Place
from test.unittest.common.test_data import (
    teardown_data,
    AppUserEncPasswordTestData1st,
    SettingCorrectTestData2ndUser1st,
    COR_SETTING_DATA_2nd,
)
from test.integtest.test_common import (
    login_form,
    place_table,
    dummy_get_position,
    nav_bar,
    saved_place_table,
)


class SavedPlaceListTests(StaticLiveServerTestCase):

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

    def search_place_to_list(self):
        """
        「テストユーザーでログイン」し、場所を検索する
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
        self.selenium.execute_script(dummy_get_position)

        # 設定２を選択し、周辺のスポットをさがすボタンを押す
        select_setting = Select(
            self.selenium.find_element_by_name("setting_now"))
        select_setting.select_by_index(1)

        self.selenium.find_element_by_xpath(
            place_table["search_button"]).click()

        # wikipediaAPI待機のため5秒待つ
        sleep(5)

    def add_place_to_list(self):
        """
        「テストユーザーでログイン」し、場所を検索し、気になるリスト追加を行う
        """
        self.search_place_to_list()
        # それぞれ気になるリストに追加するボタンを押す
        self.selenium.find_element_by_xpath(
            place_table["fav_button_first"]).click()
        self.selenium.find_element_by_xpath(
            place_table["fav_button_second"]).click()

        # 気になるリスト追加処理のため3秒待つ
        sleep(3)

    def test_saved_place_list__remove_place_from_list(self):
        """
        「テストユーザーでログイン」し、場所を検索し、気になるリスト追加の後、
        気になる場所リストから取り消しを行う
        =>気になるリストから場所を取り消しができる
        """

        # 場所表示し、気になるボタンを押した状態にする
        self.add_place_to_list()

        # 気になる場所リストに移動する
        self.selenium.find_element_by_xpath(
            nav_bar["saved_place_list"]).click()

        # 上から１つめと２つめのタイトルを変数に入れておく
        place_1_title = self.selenium.find_element_by_xpath(
            saved_place_table["title_first"]).text
        place_2_title = self.selenium.find_element_by_xpath(
            saved_place_table["title_second"]).text

        # それぞれ気になるリストから取り消すボタンを押す
        self.selenium.find_element_by_xpath(
            saved_place_table["fav_button_first"]).click()
        self.selenium.find_element_by_xpath(
            saved_place_table["fav_button_second"]).click()
        # 気になるリスト削除処理のため3秒待つ
        sleep(3)

        # 気になるリストから削除されている
        with self.assertRaises(Place.DoesNotExist):
            Place.objects.get(name=place_1_title)

        with self.assertRaises(Place.DoesNotExist):
            Place.objects.get(name=place_2_title)

    def test_saved_place_list__re_add_place_to_list(self):
        """
        「テストユーザーでログイン」し、気になる場所リストから取り消しを行った後、
        再度追加する。
        =>気になるリストに再追加ができる
        """
        # 気になる場所リストから取り消しを行った直後の状態にする
        self.test_saved_place_list__remove_place_from_list()

        # 上から１つめと２つめのタイトルを変数に入れておく
        place_1_title = self.selenium.find_element_by_xpath(
            saved_place_table["title_first"]).text
        place_2_title = self.selenium.find_element_by_xpath(
            saved_place_table["title_second"]).text

        # それぞれ気になるリストに追加ボタンを押す
        self.selenium.find_element_by_xpath(
            saved_place_table["fav_button_first"]).click()
        self.selenium.find_element_by_xpath(
            saved_place_table["fav_button_second"]).click()

        # 気になるリスト追加処理のため3秒待つ
        sleep(3)

        # 気になるリストに追加されている
        self.assertTrue(
            Place.objects.get(name=place_1_title)
        )
        self.assertTrue(
            Place.objects.get(name=place_2_title)
        )

    def test_saved_place_list__jump_to_wikipedia(self):
        """
        「テストユーザーでログイン」し、場所を検索し、画像クリックする
        =>wikipediaに移動する
        """
        # 場所表示し、気になるボタンを押した状態にする
        self.add_place_to_list()

        # 気になる場所リストに移動する
        self.selenium.find_element_by_xpath(
            nav_bar["saved_place_list"]).click()
        # ページ遷移の処理のため5秒待つ
        sleep(5)
        # 上から１つめのタイトルを変数に入れておく
        place_title = self.selenium.find_element_by_xpath(
            saved_place_table["title_first"]).text
        # 画像をクリックする
        self.selenium.find_element_by_xpath(
            saved_place_table["img_first"]).click()

        # ページ遷移の処理のため10秒待つ
        sleep(10)

        # 別タブに切り替える
        handle_array = self.selenium.window_handles
        self.selenium.switch_to.window(handle_array[-1])

        expected = Place.objects.get(name=place_title).linkUrl
        result = self.selenium.current_url

        self.assertEqual(result, expected)

    def test_saved_place_list__jump_to_googlemap(self):
        """
        「テストユーザーでログイン」し、場所を検索し、「ここへいく」ボタンを押す
        =>googlemapに移動する
        """
        # 場所表示し、気になるボタンを押した状態にする
        self.add_place_to_list()

        # 気になる場所リストに移動する
        self.selenium.find_element_by_xpath(
            nav_bar["saved_place_list"]).click()

        # 上から１つめのタイトルを変数に入れておく
        place_title = self.selenium.find_element_by_xpath(
            saved_place_table["title_first"]).text

        # 「ここへいく」ボタンをクリックする
        self.selenium.find_element_by_xpath(
            saved_place_table["search_button"]).click()
        # ページ遷移の処理のため2秒待つ(待ちすぎるとURL変わるので注意)
        sleep(2)

        # 別タブに切り替える
        handle_array = self.selenium.window_handles
        self.selenium.switch_to.window(handle_array[-1])

        latitude = Place.objects.get(name=place_title).latitude
        longtitude = Place.objects.get(name=place_title).longtitude
        latlon = str(latitude) + ',' + str(longtitude)
        google_url = 'https://www.google.com/maps/dir/'
        result = self.selenium.current_url

        self.assertTrue(google_url in result)
        self.assertTrue(latlon in result)
