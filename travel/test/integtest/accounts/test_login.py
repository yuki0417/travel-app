from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from test.unittest.common.test_data import (
    AppUserEncPasswordTestData1st,
    COR_APPUSER_DATA_1st,
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
        cls.selenium.quit()
        super().tearDownClass()

    def test_login__when_success(self):
        """
        ログイン画面にアクセスし、必要なフォーム入力し、ログインボタンを押す
        """
        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/login/'))
        # ページソースを確認
        print(self.selenium.page_source)
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys(COR_APPUSER_DATA_1st['username'])
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys(COR_APPUSER_DATA_1st['password'])
        self.selenium.find_element_by_xpath(
            '/html/body/div/div/div/form/div[3]/button').click()

        # ページソースを確認
        print(self.selenium.page_source)
        result = self.selenium.current_url
        expected = self.live_server_url + '/travel/list/'

        self.assertEqual(result, expected)
