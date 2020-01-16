from time import sleep

from django.urls import reverse_lazy
from selenium.webdriver.support.select import Select

from accounts.models import AppUser
from accounts.create_testuser import TEST_USER_INFO
from travel.models import Setting
from test.unittest.common.test_data import (
    SettingCorrectTestData2ndUser1st,
    COR_SETTING_DATA_2nd,
)


# テストユーザー名
TESTUSER_NAME = 'テストユーザー'

# ログイン画面
login_form_path = '/html/body/div/div/div/'
login_form = {
    "test_login_btn": login_form_path + 'div[1]/div/a',
    "login_btn": login_form_path + 'form/div[3]/button',
    "signup_btn": login_form_path + 'div[2]/div/a',
}

# サインアップ画面
signup_form_path = '/html/body/div/div/div/'
signup_form = {
    "register_btn": signup_form_path + 'form/div[4]/button',
}

# ナビゲーションバー
hamb_menu = '/html/body/div[1]/p'
nav_bar_path = '/html/body/div[1]/nav/'
nav_bar = {
    # 気になった場所のリンク
    "saved_place_list": nav_bar_path + 'ul/li[3]/a',
    # 検索設定のリンク
    "setting_change": nav_bar_path + 'ul/li[2]/a',
    # 設定の新規作成のリンク
    "setting_create": nav_bar_path + 'ul/li[2]/div/a[1]',
    # 設定の変更＆削除のリンク
    "setting_edit": nav_bar_path + 'ul/li[2]/div/a[2]',
    # おすすめの場所のリンク
    "shared_place": nav_bar_path + 'ul/li[4]/a',
    # ログアウトのリンク
    "logout": nav_bar_path + 'ul/li[5]/a',
}

# 場所一覧画面
# 場所一覧のテーブル
pl_tbl_path = '/html/body/div[3]/div[2]/div[3]/div[2]/div/table/tbody/'
place_table = {
    # 周辺のスポットをさがすボタン
    "search_button": '/html/body/div[3]/button',
    # １番目の気になる/取り消すボタン
    "fav_button_first": pl_tbl_path + 'tr[1]/td[1]/button',
    # ２番目の気になる/取り消すボタン
    "fav_button_second": pl_tbl_path + 'tr[2]/td[1]/button',
    # １番目のタイトル
    "title_first": pl_tbl_path + 'tr[1]/td[1]/h3',
    # ２番目のタイトル
    "title_second": pl_tbl_path + 'tr[2]/td[1]/h3',
    # １番目の画像
    "img_first": pl_tbl_path + 'tr[1]/td[1]/div/a/img',
}

# 位置情報取得スクリプトのモック
dummy_get_position = (
    "window.navigator.geolocation.getCurrentPosition="
    "function(success){"
    "const position = "
    "{\"coords\" : {"
    "\"latitude\": \"35.55555\",\"longitude\": \"139.55555\"}};"
    "success(position);}"
)

# 気になる場所リスト
# 気になる場所リストのテーブル
saved_pl_tbl_path = '/html/body/div[5]/div/div[2]/div/table/tbody/'
saved_place_table = {
    # ここへいくボタン
    "search_button": saved_pl_tbl_path + 'tr[1]/td[1]/div[3]/button',
    # １番目の気になる/取り消すボタン
    "fav_button_first": saved_pl_tbl_path + 'tr[1]/td[1]/div[2]/button',
    # ２番目の気になる/取り消すボタン
    "fav_button_second": saved_pl_tbl_path + 'tr[2]/td[1]/div[2]/button',
    # １番目のタイトル
    "title_first": saved_pl_tbl_path + 'tr[1]/td[1]/h3',
    # ２番目のタイトル
    "title_second": saved_pl_tbl_path + 'tr[2]/td[1]/h3',
    # １番目の画像
    "img_first": saved_pl_tbl_path + 'tr[1]/td[1]/div[1]/a/img',
    # １番目のおすすめするボタン
    "comment_btn": saved_pl_tbl_path + 'tr[1]/td[1]/div[4]/a',
}

# 設定作成画面
setting_create_form = {
    "create_btn": '/html/body/div[3]/div[2]/div/div/form/div/div/button',
}

# 設定編集
setting_update_form = {
    "update_btn": setting_create_form["create_btn"],
}

# 設定一覧画面
setting_tbl_path = '/html/body/div[3]/div[2]/div/table/tbody/'
setting_edit = {
    # 削除するボタン
    "delete_btn": setting_tbl_path + 'tr[1]/td[4]/a[2]',
    # 削除確認ボタン
    "delete_conf_btn": '/html/body/div[3]/div[2]/div/form/button',
    # 編集ボタン
    "edit_btn": setting_tbl_path + 'tr[1]/td[4]/a[1]',
}

# おすすめの場所作成画面
comment_form = {
    "share_btn": '/html/body/div[3]/div[2]/div/div/form/button',
}


# ログイン画面にアクセス
def open_login_page(self):
    self.selenium.get(
        '{}{}'.format(
            self.live_server_url,
            str(reverse_lazy('accounts:login'))
        )
    )


# テストユーザーでログイン
def login_with_test_user(self):
    open_login_page(self)
    self.selenium.find_element_by_xpath(
        login_form["test_login_btn"]).click()


# 新規登録画面にアクセス
def open_signup_page(self):
    self.selenium.get(
        '{}{}'.format(
            self.live_server_url,
            str(reverse_lazy('accounts:signup'))
        )
    )


def open_saved_place_page(self):
    self.selenium.get(
        '{}{}'.format(
            self.live_server_url,
            str(reverse_lazy('travel:saved_place'))
        )
    )


def open_create_setting_page(self):
    self.selenium.get(
        '{}{}'.format(
            self.live_server_url,
            str(reverse_lazy('travel:create_setting'))
        )
    )


def open_setting_list_page(self):
    self.selenium.get(
        '{}{}'.format(
            self.live_server_url,
            str(reverse_lazy('travel:setting_list'))
        )
    )


def open_logout_page(self):
    self.selenium.get(
        '{}{}'.format(
            self.live_server_url,
            str(reverse_lazy('accounts:logged_out'))
        )
    )


def open_hamb_menu(self):
    """
    「テストユーザーでログイン」し、ハンバーガーメニューを開く
    """
    # テストユーザーログイン
    login_with_test_user(self)
    self.selenium.find_element_by_xpath(hamb_menu).click()
    sleep(2)


def search_place_to_list(self):
    """
    「テストユーザーでログイン」し、場所を検索する
    """
    # テストユーザーログイン
    login_with_test_user(self)

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
    search_place_to_list(self)
    # それぞれ気になるリストに追加するボタンを押す
    self.selenium.find_element_by_xpath(
        place_table["fav_button_first"]).click()
    self.selenium.find_element_by_xpath(
        place_table["fav_button_second"]).click()

    # 気になるリスト追加処理のため3秒待つ
    sleep(3)


def move_to_share_place_page(self):
    """
    「テストユーザーでログイン」し、場所を検索し、気になるリスト追加した後、
    「他のひとにおすすめする」をクリックする
    """
    add_place_to_list(self)
    open_saved_place_page(self)
    # 「他のひとにおすすめする」ボタンをクリックする
    self.selenium.find_element_by_xpath(
        saved_place_table["comment_btn"]).click()
    # ページ遷移の処理のため2秒待つ
    sleep(2)
