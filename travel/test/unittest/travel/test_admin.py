from django.test import TestCase
from django.contrib.admin.sites import AdminSite

from travel.models import Setting, Place
from travel.admin import SettingAdmin, PlaceAdmin
from test.unittest.common.test_data import (
    AppUserCorrectTestData1st,
    SettingCorrectTestData1st,
    PlaceCorrectTestData1st,
)


class SettingAdminTestcase(TestCase):
    """
    設定情報の一覧画面のテスト
    """
    databases = '__all__'

    def setUp(self):
        AppUserCorrectTestData1st.setUp()
        SettingCorrectTestData1st.setUp()
        self.site = AdminSite()

    def test_class_variable__is_registered_correctly(self):
        sa = SettingAdmin(Setting, self.site)
        list_display = (
            'user',
            'name',
            'radius',
            'max_show_num',
        )
        self.assertEqual(sa.save_as, True)
        self.assertEqual(sa.list_display, list_display)
        self.assertEqual(sa.readonly_fields, ('id',))


class PlaceAdminTestcase(TestCase):
    """
    設定情報の一覧画面のテスト
    """
    databases = '__all__'

    def setUp(self):
        AppUserCorrectTestData1st.setUp()
        SettingCorrectTestData1st.setUp()
        PlaceCorrectTestData1st.setUp()
        self.site = AdminSite()

    def test_class_variable__is_registered_correctly(self):
        pa = PlaceAdmin(Place, self.site)
        list_display = (
            'user',
            'name',
            'saved_time',
            'linkUrl',
            'imageUrl',
            'latitude',
            'longtitude',
            'prefecture',
            'city',
        )
        self.assertEqual(pa.save_as, True)
        self.assertEqual(pa.list_display, list_display)
        self.assertEqual(pa.readonly_fields, ('id',))
