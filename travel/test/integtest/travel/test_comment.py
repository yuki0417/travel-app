from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from test.setting.selenium_setting import SELENIUM_SETTING
from travel.models import Comment
from test.unittest.common.test_data import (
    teardown_data,
    AppUserEncPasswordTestData1st,
    COR_COMMENT_DATA_1st
)
from test.integtest.test_common import (
    comment_form,
    move_to_share_place_page
)


class CommentTests(StaticLiveServerTestCase):

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

    def test_create_share_place__success(self):
        """
        「テストユーザーでログイン」し、気になる場所を作成した後、コメントを行う。
        =>コメントが作成できる
        """

        move_to_share_place_page(self)

        # コメント名を入力する。半径、最大表示件数はデフォルトのままにする。
        comment_input = self.selenium.find_element_by_name("comment")
        comment_input.send_keys(COR_COMMENT_DATA_1st['comment'])
        # 登録
        self.selenium.find_element_by_xpath(
            comment_form["share_btn"]).click()

        # コメント作成完了画面に遷移する
        result = self.selenium.find_element_by_id("result").text
        expected = "場所とコメントがシェアされました。\n気になった場所リストに戻る"
        # import pdb;pdb.set_trace()
        self.assertEqual(result, expected)

        # コメントが作成されている
        self.assertTrue(
            Comment.objects.get(comment=COR_COMMENT_DATA_1st['comment'])
        )
