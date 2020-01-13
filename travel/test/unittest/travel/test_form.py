from unittest.mock import Mock

from django.test import TestCase
from django import forms

from travel.models import Setting, Comment
from travel.forms import (
    SettingForm,
    SettingUpdateForm,
    CommentForm,
)
from test.unittest.common.test_data import (
    COR_APPUSER_DATA_1st,
    COR_SETTING_DATA_1st,
    COR_SETTING_DATA_2nd,
    AppUserCorrectTestData1st,
    SettingCorrectTestData1st,
    SettingCorrectTestData2ndUser1st,
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
    設定登録画面用のフォームのテスト
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


class MockSettingUpdateFormWithInstance(SettingUpdateForm):
    """
    設定更新画面用のフォームのcleaned_dataの値と、
    instanceの値を事前に用意しておく
    """
    cleaned_data = {
        'user': COR_APPUSER_DATA_1st['id'],
        'name': COR_SETTING_DATA_1st['name'],
    }
    # ユーザー１の設定情報２つめ
    instance = Mock()
    instance.name.return_value = COR_SETTING_DATA_2nd['name']


class MockSettingUpdateForm(SettingUpdateForm):
    """
    設定更新画面用のフォームのcleaned_dataの値を事前に用意しておく
    """
    cleaned_data = {
        'user': COR_APPUSER_DATA_1st['id'],
        'name': COR_SETTING_DATA_1st['name'],
    }


class SettingUpdateFormTestcase(TestCase):
    """
    設定更新画面用のフォームのテスト
    """
    databases = '__all__'

    def setUp(self):
        AppUserCorrectTestData1st.setUp()
        SettingCorrectTestData1st.setUp()
        SettingCorrectTestData2ndUser1st.setUp()

    def test_class_meta_variable__is_registered_correctly(self):
        meta = SettingUpdateForm(Setting).Meta()
        fields = ('user', 'name', 'radius', 'max_show_num')
        self.assertEqual(meta.model, Setting)
        self.assertEqual(meta.fields, fields)
        self.assertIsInstance(meta.widgets['user'], forms.HiddenInput)

    def test_clean__when_old_new_setting_name_same(self):
        msf = MockSettingForm(instance=Setting)
        msf.clean()
        # エラーがないのでKeyErrorとなる
        with self.assertRaises(KeyError):
            msf.errors['name'][0]

    def test_clean__when_old_new_setting_name_different(self):
        msf = MockSettingUpdateFormWithInstance(instance=Setting)
        msf.clean()
        result = msf.errors['name'][0]
        expect = '同じ設定名が存在します。違う設定名に変更してください。'
        self.assertEqual(result, expect)


class CommentFormTestcase(TestCase):
    """
    場所のコメントを登録するフォームのテスト
    """
    databases = '__all__'

    def setUp(self):
        AppUserCorrectTestData1st.setUp()
        SettingCorrectTestData1st.setUp()

    def test_class_meta_variable__is_registered_correctly(self):
        meta = CommentForm(Comment).Meta()
        fields = ('user', 'comment', 'pub_date')
        self.assertEqual(meta.model, Comment)
        self.assertEqual(meta.fields, fields)
        self.assertIsInstance(meta.widgets['user'], forms.HiddenInput)

    def test__init__(self):
        cm = CommentForm(Comment)
        self.assertTrue(
            cm.fields['pub_date'].widget.attrs['readonly']
        )
