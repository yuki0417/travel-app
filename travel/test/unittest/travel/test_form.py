from django.test import TestCase
from django import forms

from travel.models import Setting
from travel.forms import SettingForm
from test.unittest.common.test_data import (
    AppUserCorrectTestData1st,
    SettingCorrectTestData1st,
)


class SettingFormTestcase(TestCase):
    """
    設定情報の一覧画面のテスト
    """
    databases = '__all__'

    def setUp(self):
        AppUserCorrectTestData1st.setUp()
        SettingCorrectTestData1st.setUp()

    def test_class_variable__is_registered_correctly(self):
        meta = SettingForm(Setting).Meta()
        fields = ('user', 'name', 'radius', 'max_show_num')
        self.assertEqual(meta.model, Setting)
        self.assertEqual(meta.fields, fields)
        self.assertIsInstance(meta.widgets['user'], forms.HiddenInput)

    def test_init_(self):
        sf = SettingForm(Setting)
        result = sf.instance.unique_error_message('any', 'thing')
        expect = '同じ設定名が存在します。違う設定名に変更してください。'
        self.assertEqual(result, expect)
