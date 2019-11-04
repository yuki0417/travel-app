from django.test import TestCase
from django.contrib.admin.sites import AdminSite

from accounts.models import AppUser
from accounts.admin import AppUserAdmin
from test.unittest.common.test_data import (
    AppUserCorrectTestData1st,
)


class SettingAdminTestcase(TestCase):
    """
    設定情報の一覧画面のテスト
    """
    databases = '__all__'

    def setUp(self):
        AppUserCorrectTestData1st.setUp()
        self.site = AdminSite()

    def test_class_variable__is_registered_correctly(self):
        aua = AppUserAdmin(AppUser, self.site)
        list_display = (
            'id',
            'username',
            'password',
        )
        self.assertEqual(aua.save_as, True)
        self.assertEqual(aua.list_display, list_display)
        self.assertEqual(aua.readonly_fields, ('id',))
