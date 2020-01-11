from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse_lazy

from test.setting.selenium_setting import SELENIUM_SETTING
from accounts.models import AppUser
from accounts.create_testuser import TEST_USER_INFO
from travel.models import Setting
from test.unittest.common.test_data import (
    teardown_data,
    AppUserEncPasswordTestData1st,
    SettingCorrectTestData2ndUser1st,
    COR_SETTING_DATA_1st,
    COR_SETTING_DATA_2nd,
)
from test.integtest.test_common import (
    login_form,
    nav_bar,
    setting_create_form,
    setting_edit,
    setting_update_form
)


class MySeleniumTests(StaticLiveServerTestCase):

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

    def test_create_setting__success(self):
        """
        「テストユーザーでログイン」し、設定の新規作成のリンクを開き、新規に設定を作成する。
        =>設定名が重複せず、作成できる
        """
        # テストユーザーログイン
        self.login_with_test_user()

        # 「周辺を検索」の画面
        self.selenium.implicitly_wait(5)

        # 新規作成を開く
        self.selenium.find_element_by_xpath(
            nav_bar["setting_change"]).click()
        self.selenium.find_element_by_xpath(
            nav_bar["setting_create"]).click()

        # 設定名を入力する。半径、最大表示件数はデフォルトのままにする。
        name_input = self.selenium.find_element_by_name("name")
        name_input.send_keys(COR_SETTING_DATA_1st['name'])
        # 登録
        self.selenium.find_element_by_xpath(
            setting_create_form["create_btn"]).click()

        # 設定作成完了画面に遷移する
        result = self.selenium.current_url
        expected = \
            self.live_server_url + str(reverse_lazy('travel:done_setting'))
        self.assertEqual(result, expected)

        # 設定が作成されている
        self.assertTrue(
            Setting.objects.get(name=COR_SETTING_DATA_1st['name'])
        )

    def test_create_setting__failed(self):
        """
        「テストユーザーでログイン」し、設定の新規作成のリンクを開き、新規に設定を作成する。
        =>設定名が重複して、作成できない。
        """
        # あらかじめ設定を作成しておく
        self.test_create_setting__success()
        # テストユーザーログイン
        self.login_with_test_user()

        # 「周辺を検索」の画面
        self.selenium.implicitly_wait(5)
        # 新規作成を開く
        self.selenium.find_element_by_xpath(
            nav_bar["setting_change"]).click()
        self.selenium.find_element_by_xpath(
            nav_bar["setting_create"]).click()

        # 設定名を入力する。
        name_input = self.selenium.find_element_by_name("name")
        name_input.send_keys(COR_SETTING_DATA_1st['name'])

        self.selenium.find_element_by_xpath(
            setting_create_form["create_btn"]).click()

        # 重複エラーになり、ページ遷移しない
        result = self.selenium.current_url
        expected = \
            self.live_server_url + str(reverse_lazy('travel:create_setting'))

        self.assertEqual(result, expected)

    def test_delete_setting__success(self):
        """
        「テストユーザーでログイン」し、設定の変更＆削除のリンクを開き、設定を削除する。
        =>設定名が削除されている。
        """
        # あらかじめ設定を作成しておく
        self.test_create_setting__success()
        # テストユーザーログイン
        self.login_with_test_user()

        # 「周辺を検索」の画面
        self.selenium.implicitly_wait(5)
        # 変更＆削除を開く
        self.selenium.find_element_by_xpath(
            nav_bar["setting_change"]).click()
        self.selenium.find_element_by_xpath(
            nav_bar["setting_edit"]).click()

        # 削除するボタンをクリックする
        self.selenium.find_element_by_xpath(
            setting_edit["delete_btn"]).click()

        # 確認画面でも続けて削除するボタンをクリックする
        self.selenium.find_element_by_xpath(
            setting_edit["delete_conf_btn"]).click()

        # 変更＆削除を開く
        self.selenium.get(
            '%s%s' % (
                self.live_server_url,
                str(reverse_lazy('travel:setting_list'))))

        # 設定画面に何も表示されていないので削除ボタンを押せない
        with self.assertRaises(NoSuchElementException):
            self.selenium.find_element_by_xpath(
                setting_edit["delete_btn"]).click()

    def test_update_setting__success(self):
        """
        「テストユーザーでログイン」し、設定の変更＆削除のリンクを開き、設定を編集する。
        =>設定名が変更されている
        """
        # あらかじめ設定を作成しておく
        self.test_create_setting__success()
        # テストユーザーログイン
        self.login_with_test_user()

        # 設定のオブジェクトのIDを最後の確認のため取得しておく
        test_setting = Setting.objects.get(name=COR_SETTING_DATA_1st['name'])
        test_setting_id = test_setting.id

        # 「周辺を検索」の画面
        self.selenium.implicitly_wait(5)
        # 変更＆削除を開く
        self.selenium.find_element_by_xpath(
            nav_bar["setting_change"]).click()
        self.selenium.find_element_by_xpath(
            nav_bar["setting_edit"]).click()

        # 編集するボタンをクリックする
        self.selenium.find_element_by_xpath(
            setting_edit["edit_btn"]).click()

        # 設定名を変更する
        name_input = self.selenium.find_element_by_name("name")
        name_input.clear()
        name_input.send_keys(COR_SETTING_DATA_2nd['name'])

        self.selenium.find_element_by_xpath(
            setting_update_form["update_btn"]).click()

        # 設定変更完了画面に遷移する
        result = self.selenium.current_url
        expected = \
            self.live_server_url + str(
                reverse_lazy('travel:setting_update_done'))
        self.assertEqual(result, expected)

        # 設定名が変更されている
        changed_setting = Setting.objects.get(id=test_setting_id)
        self.assertEqual(COR_SETTING_DATA_2nd['name'], changed_setting.name)

    def test_update_setting__failed(self):
        """
        「テストユーザーでログイン」し、設定の変更＆削除のリンクを開き、設定を編集する。
        =>「設定2」が重複するため、設定名が変更できない
        """
        # テストユーザーログイン
        self.login_with_test_user()
        # 設定2のuserをユニットテストユーザーからテストユーザーに変更しておく
        SettingCorrectTestData2ndUser1st.setUp()
        test_setting_2nd = Setting.objects.get(id=COR_SETTING_DATA_2nd["id"])
        test_setting_2nd.user = \
            AppUser.objects.get(username=TEST_USER_INFO['username'])
        test_setting_2nd.save()
        # あらかじめ設定を作成しておく
        self.test_create_setting__success()

        # 「周辺を検索」の画面
        self.selenium.implicitly_wait(5)
        # 変更＆削除を開く
        self.selenium.find_element_by_xpath(
            nav_bar["setting_change"]).click()
        self.selenium.find_element_by_xpath(
            nav_bar["setting_edit"]).click()

        # 編集するボタンをクリックする
        self.selenium.find_element_by_xpath(
            setting_edit["edit_btn"]).click()

        # 設定名を変更する
        name_input = self.selenium.find_element_by_name("name")
        name_input.clear()
        name_input.send_keys(COR_SETTING_DATA_2nd['name'])

        # 最後の比較のためURLを記録しておく
        current_url = self.selenium.current_url

        self.selenium.find_element_by_xpath(
            setting_update_form["update_btn"]).click()

        # 設定変更画面のままになる
        result = self.selenium.current_url
        expected = current_url
        self.assertEqual(result, expected)
