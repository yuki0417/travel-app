from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse_lazy

from accounts.models import AppUser
from accounts.create_testuser import TEST_USER_INFO
from travel.models import Setting
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

    def test_create_setting__success(self):
        """
        「テストユーザーでログイン」し、設定の新規作成のリンクを開き、新規に設定を作成する。
        =>設定名が重複せず、作成できる
        """
        # テストユーザーログイン
        self.login_with_test_user()

        # 「周辺を検索」の画面
        self.selenium.implicitly_wait(5)
        self.selenium.find_element_by_xpath(
            '/html/body/nav/ul/li[2]/a').click()
        # 新規作成を開く
        self.selenium.find_element_by_xpath(
            '/html/body/nav/ul/li[2]/div/a[1]').click()

        # 設定名を入力する。半径、最大表示件数はデフォルトのままにする。
        setting_name_input = self.selenium.find_element_by_name("name")
        setting_name_input.send_keys(COR_SETTING_DATA_1st['name'])

        self.selenium.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div/div/form/div/div/button').click()

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
        self.selenium.find_element_by_xpath(
            '/html/body/nav/ul/li[2]/a').click()
        # 新規作成を開く
        self.selenium.find_element_by_xpath(
            '/html/body/nav/ul/li[2]/div/a[1]').click()

        # 設定名を入力する。
        setting_name_input = self.selenium.find_element_by_name("name")
        setting_name_input.send_keys(COR_SETTING_DATA_1st['name'])

        self.selenium.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div/div/form/div/div/button').click()

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
        delete_button = \
            '/html/body/div[2]/div[2]/div/table/tbody/tr[1]/td[4]/a[2]'
        # あらかじめ設定を作成しておく
        self.test_create_setting__success()
        # テストユーザーログイン
        self.login_with_test_user()

        # 「周辺を検索」の画面
        self.selenium.implicitly_wait(5)
        self.selenium.find_element_by_xpath(
            '/html/body/nav/ul/li[2]/a').click()
        # 変更＆削除を開く
        self.selenium.find_element_by_xpath(
            '/html/body/nav/ul/li[2]/div/a[2]').click()

        # 削除するボタンをクリックする
        self.selenium.find_element_by_xpath(delete_button).click()

        # 確認画面でも続けて削除するボタンをクリックする
        self.selenium.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div/form/button'
            ).click()

        # 変更＆削除を開く
        self.selenium.get(
            '%s%s' % (
                self.live_server_url,
                str(reverse_lazy('travel:setting_list'))))

        # 設定画面に何も表示されていないので削除ボタンを押せない
        with self.assertRaises(NoSuchElementException):
            self.selenium.find_element_by_xpath(delete_button).click()

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
        self.selenium.find_element_by_xpath(
            '/html/body/nav/ul/li[2]/a').click()
        # 変更＆削除を開く
        self.selenium.find_element_by_xpath(
            '/html/body/nav/ul/li[2]/div/a[2]').click()

        # 編集するボタンをクリックする
        self.selenium.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div/table/tbody/tr[1]/td[4]/a[1]'
            ).click()

        # 設定名を変更する
        setting_name_input = self.selenium.find_element_by_name("name")
        setting_name_input.clear()
        setting_name_input.send_keys(COR_SETTING_DATA_2nd['name'])

        self.selenium.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div/div/form/div/div/button').click()

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
        self.selenium.find_element_by_xpath(
            '/html/body/nav/ul/li[2]/a').click()
        # 変更＆削除を開く
        self.selenium.find_element_by_xpath(
            '/html/body/nav/ul/li[2]/div/a[2]').click()

        # 編集するボタンをクリックする
        self.selenium.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div/table/tbody/tr[1]/td[4]/a[1]'
            ).click()

        # 設定名を変更する
        setting_name_input = self.selenium.find_element_by_name("name")
        setting_name_input.clear()
        setting_name_input.send_keys(COR_SETTING_DATA_2nd['name'])

        # 最後の比較のためURLを記録しておく
        current_url = self.selenium.current_url
        # import pdb;pdb.set_trace()

        self.selenium.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div/div/form/div/div/button').click()

        # 設定変更画面のままになる
        result = self.selenium.current_url
        expected = current_url
        self.assertEqual(result, expected)
