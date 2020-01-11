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
nav_bar_path = '/html/body/nav/'
nav_bar = {
    # 気になる場所リストのリンク
    "saved_place_list": nav_bar_path + 'ul/li[3]/a',
    # 設定の作成＆変更のリンク
    "setting_change": nav_bar_path + 'ul/li[2]/a',
    # 設定の新規作成のリンク
    "setting_create": nav_bar_path + 'ul/li[2]/div/a[1]',
    # 設定の変更＆削除のリンク
    "setting_edit": nav_bar_path + 'ul/li[2]/div/a[2]',
}

# 場所一覧画面
# 場所一覧のテーブル
pl_tbl_path = '/html/body/div[3]/div[3]/div[2]/div/table/tbody/'
place_table = {
    # 周辺のスポットをさがすボタン
    "search_button": '/html/body/div[2]/button',
    # １番目の気になる/取り消すボタン
    "fav_button_first": pl_tbl_path + 'tr[1]/td[1]/button',
    # ２番目の気になる/取り消すボタン
    "fav_button_second": pl_tbl_path + 'tr[2]/td[1]/button',
    # １番目のタイトル
    "title_first": pl_tbl_path + 'tr[1]/td[1]/h3',
    # ２番目のタイトル
    "title_second": pl_tbl_path + 'tr[2]/td[1]/h3',
    # １番目の画像
    "img_first": pl_tbl_path + 'tr[1]/td[1]/class/a/img',
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
saved_pl_tbl_path = '/html/body/div[4]/div/div[2]/div/table/tbody/'
saved_place_table = {
    # ここへいくボタン
    "search_button": saved_pl_tbl_path + 'tr/td[1]/class[3]/button',
    # １番目の気になる/取り消すボタン
    "fav_button_first": saved_pl_tbl_path + 'tr[1]/td[1]/class[2]/button',
    # ２番目の気になる/取り消すボタン
    "fav_button_second": saved_pl_tbl_path + 'tr[2]/td[1]/class[2]/button',
    # １番目のタイトル
    "title_first": saved_pl_tbl_path + 'tr[1]/td[1]/h3',
    # ２番目のタイトル
    "title_second": saved_pl_tbl_path + 'tr[2]/td[1]/h3',
    # １番目の画像
    "img_first": saved_pl_tbl_path + 'tr[1]/td[1]/class[1]/a/img',
}

# 設定作成画面
setting_create_form = {
    "create_btn": '/html/body/div[2]/div[2]/div/div/form/div/div/button',
}

# 設定一覧画面
setting_tbl_path = '/html/body/div[2]/div[2]/div/table/tbody/'
setting_edit = {
    # 削除するボタン
    "delete_btn": setting_tbl_path + 'tr[1]/td[4]/a[2]',
    # 削除確認ボタン
    "delete_conf_btn": '/html/body/div[2]/div[2]/div/form/button',
    # 編集ボタン
    "edit_btn": setting_tbl_path + 'tr[1]/td[4]/a[1]',
}

# 設定編集
setting_update_form = {
    "update_btn": '/html/body/div[2]/div[2]/div/div/form/div/div/button'
}
