from django.test import TestCase
from django import forms

from travel.models import Setting
from travel.forms import SettingForm, SettingUpdateForm
from test.unittest.common.test_data import (
    COR_APPUSER_DATA_1st,
    COR_SETTING_DATA_1st,
    AppUserCorrectTestData1st,
    SettingCorrectTestData1st,
)


class MockSettingForm(SettingForm):
    """
    設定フォームのcleaned_dataの値を事前に用意しておく
    """
    cleaned_data = {
        'user': COR_APPUSER_DATA_1st['id'],
        'name': COR_SETTING_DATA_1st['name'],
    }


class SettingFormTestcase(TestCase):
    """
    設定情報の一覧画面のテスト
    """
    databases = '__all__'

    def setUp(self):
        AppUserCorrectTestData1st.setUp()
        SettingCorrectTestData1st.setUp()

    def test_class_meta_variable__is_registered_correctly(self):
        meta = SettingForm(Setting).Meta()
        fields = ('user', 'name', 'radius', 'max_show_num')
        self.assertEqual(meta.model, Setting)
        self.assertEqual(meta.fields, fields)
        self.assertIsInstance(meta.widgets['user'], forms.HiddenInput)

    def test_clean(self):
        msf = MockSettingForm(instance=Setting)
        msf.clean()
        result = msf.errors['name'][0]
        expect = '同じ設定名が存在します。違う設定名に変更してください。'
        self.assertEqual(result, expect)


class SettingUpdateFormTestcase(TestCase):
    """
    設定情報の一覧画面のテスト
    """
    databases = '__all__'

    def setUp(self):
        AppUserCorrectTestData1st.setUp()
        SettingCorrectTestData1st.setUp()

    def test_class_meta_variable__is_registered_correctly(self):
        meta = SettingUpdateForm(Setting).Meta()
        fields = ('user', 'name', 'radius', 'max_show_num')
        self.assertEqual(meta.model, Setting)
        self.assertEqual(meta.fields, fields)
        self.assertIsInstance(meta.widgets['user'], forms.HiddenInput)
