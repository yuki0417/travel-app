import copy
from unittest.mock import patch, MagicMock, Mock
from io import StringIO, BytesIO

from django.core.handlers.wsgi import WSGIRequest
from django.test import TestCase, TransactionTestCase
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
)
from django.shortcuts import render
from django.urls import reverse_lazy

from test_plus.test import CBVTestCase

from travel.views import (
    PlaceListView,
    SettingCreateView,
    SettingListView,
    SettingUpdateView,
    SettingDeleteView,
    SavedPlaceListView,
    setting_done,
    delete_done,
    place_save,
    place_delete
)
from travel.models import Place, Setting
from travel.forms import SettingForm
from travel.wikipedia import geo_search
from accounts.models import AppUser
from test.unittest.common.test_data import (
    COR_APPUSER_DATA_1st,
    COR_APPUSER_DATA_2nd,
    COR_SETTING_DATA_1st,
    COR_SETTING_DATA_2nd,
    COR_PLACE_DATA_1st,
    COR_PLACE_DATA_2nd,
    AppUserCorrectTestData1st,
    AppUserCorrectTestData2nd,
    SettingCorrectTestData1st,
    SettingCorrectTestData2nd,
    PlaceCorrectTestData1st,
    PlaceCorrectTestData2nd,
    WIKI_PLACE_LIST_SAVED_EXIST
)


class MockPlaceListView1st(PlaceListView):
    """
    WSGIのモックを含めたPlaceListViewを定義する
    """
    request = Mock()
    request.session.get = MagicMock(
        return_value=COR_APPUSER_DATA_1st['id'])


class MockPlaceListView2nd(PlaceListView):
    """
    WSGIのモックを含めたPlaceListViewを定義する
    """
    request = Mock()
    request.session.get = MagicMock(
        return_value=COR_APPUSER_DATA_2nd['id'])


# CBVTestCaseはコンテキストデータのテストに便利（get_instanceメソッドなど）
class PlaceListViewTestcase(CBVTestCase):
    """
    設定情報の正常データが登録されるかチェック
    """
    databases = '__all__'        

    def setUp(self):
        AppUserCorrectTestData1st.setUp()
        SettingCorrectTestData1st.setUp()

    def test_class_variable__is_registered_correctly(self):
        plv = PlaceListView()
        self.assertEqual(
            plv.template_name,
            'travel/place_list.html'
        )
        self.assertEqual(
            plv.setting_radius_meta,
            Setting._meta.get_field('radius').verbose_name
        )
        self.assertEqual(
            plv.setting_max_show_num_meta,
            Setting._meta.get_field('max_show_num').verbose_name
        )

    # クエリが存在する場合
    def test_get_queryset__with_queryset(self):
        plv_1st = MockPlaceListView1st()
        result = plv_1st.get_queryset()
        expect = Setting.objects.filter(user=COR_APPUSER_DATA_1st['id'])
        self.assertQuerysetEqual(result, expect, transform=lambda x: x)

    # クエリが存在しない場合
    def test_get_queryset__with_no_queryset(self):
        AppUserCorrectTestData2nd.setUp()
        plv_2nd = MockPlaceListView2nd()
        result = plv_2nd.get_queryset()
        expect = Setting.objects.filter(user=COR_APPUSER_DATA_2nd['id'])
        self.assertQuerysetEqual(result, expect, transform=lambda x: x)

    def test_get_context_data(self):
        plv = self.get_instance(
            PlaceListView,
            initkwargs={'object_list': ''})
        context = plv.get_context_data()
        self.assertEqual(
            context['setting_radius_meta'],
            plv.setting_radius_meta
        )
        self.assertEqual(
            context['setting_max_show_num_meta'],
            plv.setting_max_show_num_meta
        )

    def test_mark_saved_place(self):
        PlaceCorrectTestData1st.setUp()
        user = AppUser.objects.get(id=COR_APPUSER_DATA_1st['id'])
        place_raw_list = WIKI_PLACE_LIST_SAVED_EXIST
        plv = PlaceListView()
        result = plv.mark_saved_place(user, place_raw_list)
        self.assertEqual(result[0]['saved'], True)
        self.assertEqual(result[1]['saved'], False)
