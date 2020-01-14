import re
from unittest.mock import patch, MagicMock, Mock
from io import StringIO

from django.core.handlers.wsgi import WSGIRequest
from django.test import TestCase, RequestFactory
from django.shortcuts import render
from django.urls import reverse_lazy
from django.db.models.query import QuerySet

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
    place_delete,
    setting_update_done,
    SharePlaceView,
    SharedPlaceListView,
)
from travel.models import (
    Place,
    Setting,
    Comment,
    SharedPlace,
    PlaceComment,
)    
from travel.forms import (
    SettingForm,
    SettingUpdateForm,
    CommentForm
)
from accounts.models import AppUser
from test.unittest.common.test_data import (
    COR_APPUSER_DATA_1st,
    COR_APPUSER_DATA_2nd,
    COR_SETTING_DATA_1st,
    COR_PLACE_DATA_1st,
    COR_COMMENT_DATA_1st,
    COR_SHA_PLACE_DATA_1st,
    COR_SHA_PLACE_DATA_2nd,
    COR_PLC_COMMT_1st,
    AppUserCorrectTestData1st,
    AppUserCorrectTestData2nd,
    SettingCorrectTestData1st,
    PlaceCorrectTestData1st,
    CommentCorrectTestData1st,
    SharedPlaceCorrectTestData1st,
    SharedPlaceCorrectTestData2nd,
    PlaceCommentCorrectTestData1st,
    WIKI_PLACE_LIST_SAVED_EXIST,
    YOUR_LOCATION,
    WIKI_PLACE_LIST,
    PLACE_LIST_SAVED_MARKED,
)


context_1st = {
    'user_id': COR_APPUSER_DATA_1st['id'],
    'username': COR_APPUSER_DATA_1st['username'],
    'last_login': COR_APPUSER_DATA_1st['last_login'],
}


# htmlの比較の際にcsrfトークンの部分を取り除く関数
def remove_csrf(html_code):
    csrf_regex = r'csrfmiddlewaretoken.*\n'
    return re.sub(csrf_regex, '', html_code)


# WSGIRequest利用の際に呼び出すセッションデータのモックを作成する関数
def mock_wsgi_session_context():
    SessionStore = Mock()
    SessionStore.return_value.get.return_value = \
        COR_APPUSER_DATA_1st['id']
    WSGIRequest.session = SessionStore()


class MockPlaceListView1st(PlaceListView):
    """
    ユーザー１のセッションを再現するために、
    WSGIのモックを含めたPlaceListViewを定義する
    """
    request = Mock()
    request.session.get = MagicMock(
        return_value=COR_APPUSER_DATA_1st['id'])


class MockPlaceListView2nd(PlaceListView):
    """
    ユーザー２のセッションを再現するために、
    WSGIのモックを含めたPlaceListViewを定義する
    """
    request = Mock()
    request.session.get = MagicMock(
        return_value=COR_APPUSER_DATA_2nd['id'])


# CBVTestCaseはコンテキストデータのテストに便利（get_instanceメソッドなど）
class PlaceListViewTestcase(CBVTestCase):
    """
    場所情報表示画面のテスト
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

    @patch(
        'travel.views.geo_search',
        MagicMock(return_value=WIKI_PLACE_LIST))
    @patch(
        'travel.views.PlaceListView.mark_saved_place',
        MagicMock(return_value=PLACE_LIST_SAVED_MARKED))
    def test_post__with_place_raw_list_exists(self):
        mock_wsgi_session_context()

        WSGIRequest.POST = Mock()
        WSGIRequest.POST.get = MagicMock(
            return_value=COR_SETTING_DATA_1st['id'])
        WSGIRequest.POST.getlist = MagicMock(
            return_value=YOUR_LOCATION)
        post_request = WSGIRequest({
            'REQUEST_METHOD': 'POST',
            'PATH_INFO': 'travel:place_list',
            'wsgi.input': StringIO()})

        plv = PlaceListView()
        result = plv.post(post_request)

        d = {
            'your_location': YOUR_LOCATION,
            'place_list': PLACE_LIST_SAVED_MARKED,
            'radius': COR_SETTING_DATA_1st['radius'],
            'max_show_num': COR_SETTING_DATA_1st['max_show_num'],
        }
        expect = render(post_request, 'travel/place_result.html', d)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(
            remove_csrf(result.content.decode('utf-8')),
            remove_csrf(expect.content.decode('utf-8'))
        )

    @patch(
        'travel.views.geo_search',
        MagicMock(return_value=None))
    @patch(
        'travel.views.PlaceListView.mark_saved_place',
        MagicMock(return_value=PLACE_LIST_SAVED_MARKED))
    def test_post__with_place_raw_list_none(self):
        mock_wsgi_session_context()

        WSGIRequest.POST = Mock()
        WSGIRequest.POST.get = MagicMock(
            return_value=COR_SETTING_DATA_1st['id'])
        WSGIRequest.POST.getlist = MagicMock(
            return_value=YOUR_LOCATION)
        post_request = WSGIRequest({
            'REQUEST_METHOD': 'POST',
            'PATH_INFO': 'travel:place_list',
            'wsgi.input': StringIO()})
        plv = PlaceListView()
        result = plv.post(post_request)

        expect = render(post_request, 'travel/place_not_found.html')

        self.assertEqual(result.status_code, 200)
        self.assertEqual(
            remove_csrf(result.content.decode('utf-8')),
            remove_csrf(expect.content.decode('utf-8'))
        )


class SettingCreateViewTestcase(TestCase):
    """
    設定作成用ビューのテスト
    """
    databases = '__all__'

    def test_class_variable__is_registered_correctly(self):
        scv = SettingCreateView()
        self.assertEqual(scv.model, Setting)
        self.assertEqual(scv.form_class, SettingForm)
        self.assertEqual(
            scv.template_name,
            'travel/setting_form.html'
        )
        self.assertEqual(
            scv.success_url,
            reverse_lazy('travel:done_setting')
        )


class SettingDoneTestcase(TestCase):
    """
    設定完了画面のテスト
    """
    databases = '__all__'

    def setUp(self):
        AppUserCorrectTestData1st.setUp()
        SettingCorrectTestData1st.setUp()

    def test_setting_done(self):
        request = WSGIRequest({
            'REQUEST_METHOD': 'GET',
            'PATH_INFO': 'travel:done_setting',
            'wsgi.input': StringIO()})
        mock_wsgi_session_context()

        expect = render(request, 'travel/setting_done.html')
        result = setting_done(request)
        self.assertEqual(
            remove_csrf(result.content.decode('utf-8')),
            remove_csrf(expect.content.decode('utf-8'))
        )


class MockSettingListView1st(SettingListView):
    """
    ユーザー１のセッションを再現するために、
    WSGIのモックを含めたSettingListViewを定義する
    """
    request = Mock()
    request.session.get = MagicMock(
        return_value=COR_APPUSER_DATA_1st['id'])


class SettingListViewTestcase(TestCase):
    """
    設定情報の一覧画面のテスト
    """
    databases = '__all__'

    def setUp(self):
        AppUserCorrectTestData1st.setUp()
        SettingCorrectTestData1st.setUp()

    def test_class_variable__is_registered_correctly(self):
        slv = SettingListView()
        self.assertEqual(slv.model, Setting)
        self.assertEqual(slv.template_name, 'travel/setting_list.html')

    def test_queryset(self):
        mock_wsgi_session_context()
        expect = Setting.objects.filter(user=COR_APPUSER_DATA_1st['id'])
        slv_1st = MockSettingListView1st()
        result = slv_1st.queryset()
        self.assertQuerysetEqual(result, expect, transform=lambda x: x)


class MockSettingUpdateView(SettingUpdateView):
    """
    設定１の選択状態を再現するために、
    引数をあらかじめ追加したSettingUpdateViewを定義する
    """
    kwargs = {'id': COR_SETTING_DATA_1st['id']}


class SettingUpdateViewTestcase(TestCase):
    """
    設定の更新画面のテスト
    """
    databases = '__all__'

    def setUp(self):
        AppUserCorrectTestData1st.setUp()
        SettingCorrectTestData1st.setUp()

    def test_class_variable__is_registered_correctly(self):
        sdv = SettingUpdateView()
        self.assertEqual(sdv.model, Setting)
        self.assertEqual(sdv.form_class, SettingUpdateForm)
        self.assertEqual(
            sdv.success_url,
            reverse_lazy('travel:setting_update_done'))

    def test_get_object(self):
        sdv = MockSettingUpdateView()
        result = sdv.get_object()
        expect = Setting.objects.get(id=COR_SETTING_DATA_1st['id'])
        self.assertEqual(result, expect)


class UpdateDoneTestcase(TestCase):
    """
    設定更新完了画面のテスト
    """
    databases = '__all__'

    def setUp(self):
        AppUserCorrectTestData1st.setUp()
        SettingCorrectTestData1st.setUp()

    def test_setting_update_done(self):
        request = WSGIRequest({
            'REQUEST_METHOD': 'GET',
            'PATH_INFO': 'travel:done_setting',
            'wsgi.input': StringIO()})
        mock_wsgi_session_context()

        expect = render(request, 'travel/setting_update_done.html')
        result = setting_update_done(request)
        self.assertEqual(
            remove_csrf(result.content.decode('utf-8')),
            remove_csrf(expect.content.decode('utf-8'))
        )


class MockSettingDeleteView(SettingDeleteView):
    """
    設定１の選択状態を再現するために、
    引数をあらかじめ追加したSettingDeleteViewを定義する
    """
    kwargs = {'id': COR_SETTING_DATA_1st['id']}


class SettingDeleteViewTestcase(TestCase):
    """
    設定の削除画面のテスト
    """
    databases = '__all__'

    def setUp(self):
        AppUserCorrectTestData1st.setUp()
        SettingCorrectTestData1st.setUp()

    def test_class_variable__is_registered_correctly(self):
        sdv = SettingDeleteView()
        self.assertEqual(sdv.model, Setting)
        self.assertEqual(
            sdv.success_url,
            reverse_lazy('travel:setting_delete_done'))

    def test_get_object(self):
        sdv = MockSettingDeleteView()
        result = sdv.get_object()
        expect = Setting.objects.get(id=COR_SETTING_DATA_1st['id'])
        self.assertEqual(result, expect)


class DeleteDoneTestcase(TestCase):
    """
    削除完了画面のテスト
    """
    databases = '__all__'

    def setUp(self):
        AppUserCorrectTestData1st.setUp()
        SettingCorrectTestData1st.setUp()

    def test_delete_done(self):
        request = WSGIRequest({
            'REQUEST_METHOD': 'GET',
            'PATH_INFO': 'travel:done_setting',
            'wsgi.input': StringIO()})
        mock_wsgi_session_context()

        expect = render(request, 'travel/setting_delete_done.html')
        result = delete_done(request)
        self.assertEqual(
            remove_csrf(result.content.decode('utf-8')),
            remove_csrf(expect.content.decode('utf-8'))
        )


class PlaceSaveTestcase(TestCase):
    """
    場所保存リクエストのテスト
    """
    databases = '__all__'

    def setUp(self):
        AppUserCorrectTestData1st.setUp()

    def test_place_save__with_post_method(self):
        request = WSGIRequest({
            'REQUEST_METHOD': 'POST',
            'wsgi.input': StringIO()})
        mock_wsgi_session_context()
        WSGIRequest.POST = Mock()
        side_effect = [
            WIKI_PLACE_LIST[0]['name'],
            WIKI_PLACE_LIST[0]['linkUrl'],
            WIKI_PLACE_LIST[0]['imageUrl'],
            WIKI_PLACE_LIST[0]['extract'],
            WIKI_PLACE_LIST[0]['latitude'],
            WIKI_PLACE_LIST[0]['longtitude'],
            COR_PLACE_DATA_1st['prefecture'],
            COR_PLACE_DATA_1st['city'],
        ]
        WSGIRequest.POST.get = MagicMock(
            side_effect=side_effect)

        expect = render(request, 'travel/place_result.html')
        result = place_save(request)
        self.assertEqual(
            remove_csrf(result.content.decode('utf-8')),
            remove_csrf(expect.content.decode('utf-8'))
        )

    def test_place_save__with_no_post_method(self):
        request = WSGIRequest({
            'REQUEST_METHOD': 'GET',
            'wsgi.input': StringIO()})
        result = place_save(request)
        self.assertEqual(result, None)


class PlaceDeleteTestcase(TestCase):
    """
    場所取り消しのテスト
    """
    databases = '__all__'

    def setUp(self):
        AppUserCorrectTestData1st.setUp()
        PlaceCorrectTestData1st.setUp()

    def test_place_delete__with_post_method(self):
        request = WSGIRequest({
            'REQUEST_METHOD': 'POST',
            'wsgi.input': StringIO()})
        mock_wsgi_session_context()
        WSGIRequest.POST = Mock()
        WSGIRequest.POST.get = MagicMock(
            return_value=COR_PLACE_DATA_1st['name'])

        expect = render(request, 'travel/place_result.html')
        result = place_delete(request)
        self.assertEqual(
            remove_csrf(result.content.decode('utf-8')),
            remove_csrf(expect.content.decode('utf-8'))
        )

    def test_place_delete__with_no_post_method(self):
        request = WSGIRequest({
            'REQUEST_METHOD': 'GET',
            'wsgi.input': StringIO()})
        result = place_delete(request)
        self.assertEqual(result, None)


class MockSavedPlaceListView(SavedPlaceListView):
    """
    ユーザー１のセッションを再現するために、
    WSGIのモックを含めたSavedPlaceListViewを定義する
    """
    request = Mock()
    request.session.get = MagicMock(
        return_value=COR_APPUSER_DATA_1st['id'])


class SavedPlaceListViewTestcase(TestCase):
    """
    気になるリストの一覧画面のテスト
    """
    databases = '__all__'

    def setUp(self):
        AppUserCorrectTestData1st.setUp()
        PlaceCorrectTestData1st.setUp()

    def test_class_variable__is_registered_correctly(self):
        splv = SavedPlaceListView()
        self.assertEqual(
            splv.template_name,
            'travel/saved_place_list.html')

    def test_get_queryset(self):
        splv = MockSavedPlaceListView()
        result = splv.get_queryset()
        expect = Place.objects.filter(user=COR_APPUSER_DATA_1st['id'])
        self.assertQuerysetEqual(result, expect, transform=lambda x: x)


class MockSharePlaceView(SharePlaceView):
    """
    設定１の選択状態を再現するために、
    引数をあらかじめ追加したSettingUpdateViewを定義する
    """
    kwargs = {'id': COR_PLACE_DATA_1st["id"]}


# CBVTestCaseはコンテキストデータのテストに便利（get_instanceメソッドなど）
class SharePlaceViewTestcase(CBVTestCase):
    """
    場所情報表示画面のテスト
    """
    databases = '__all__'

    def setUp(self):
        AppUserCorrectTestData1st.setUp()
        PlaceCorrectTestData1st.setUp()
        SharedPlaceCorrectTestData1st.setUp()

    def test_class_variable__is_registered_correctly(self):
        spv = SharePlaceView()
        self.assertEqual(spv.model, Comment)
        self.assertEqual(spv.form_class, CommentForm)
        self.assertEqual(
            spv.template_name,
            'travel/comment_form.html'
        )

    def test_get_object(self):
        spv = MockSharePlaceView()
        self.assertEqual(
            Place.objects.get(id=COR_PLACE_DATA_1st["id"]),
            spv.get_object()
        )

    def test_get_context_data(self):
        spv = SharePlaceView()
        # モックにさしかえ
        mock_obj = Place.objects.get(id=COR_PLACE_DATA_1st["id"])
        spv.get_object = MagicMock(return_value=mock_obj)
        request = RequestFactory().get('/')
        spv.setup(request)
        context = spv.get_context_data()
        self.assertEqual(context['place'], mock_obj)

    @patch(
        'travel.views.SharePlaceView.save_comment',
        MagicMock(return_value=None))
    @patch(
        'travel.views.SharePlaceView.add_to_sharedplace',
        MagicMock(return_value=None))
    @patch(
        'travel.views.SharePlaceView.connect_comment_place',
        MagicMock(return_value=None))
    def test_post(self):
        mock_wsgi_session_context()

        WSGIRequest.POST = MagicMock(
            {
                "user": COR_COMMENT_DATA_1st["user"],
                "comment": COR_COMMENT_DATA_1st["comment"],
                "pub_date": COR_COMMENT_DATA_1st["pub_date"],
                "name": COR_SHA_PLACE_DATA_1st["name"],
                "linkUrl": COR_SHA_PLACE_DATA_1st["linkUrl"],
                "imageUrl": COR_SHA_PLACE_DATA_1st["imageUrl"],
                "extract": COR_SHA_PLACE_DATA_1st["extract"],
                "latitude": COR_SHA_PLACE_DATA_1st["latitude"],
                "longtitude": COR_SHA_PLACE_DATA_1st["longtitude"],
            }
        )
        post_request = WSGIRequest({
            'REQUEST_METHOD': 'POST',
            'PATH_INFO': 'travel:place_list',
            'wsgi.input': StringIO()})
        spv = SharePlaceView()
        result = spv.post(post_request)
        expect = render(post_request, 'travel/share_place_done.html')

        self.assertEqual(result.status_code, 200)
        self.assertEqual(
            remove_csrf(result.content.decode('utf-8')),
            remove_csrf(expect.content.decode('utf-8'))
        )

    def test_save_comment(self):
        spv = SharePlaceView()
        comment = {
            'user': COR_COMMENT_DATA_1st["user"],
            'comment': COR_COMMENT_DATA_1st["comment"],
            'pub_date': COR_COMMENT_DATA_1st["pub_date"],
        }
        # インスタンス自身は不明なので、該当するオブジェクトができているか確認する
        spv.save_comment(comment)
        self.assertTrue(
            Comment.objects.get(
                user=COR_COMMENT_DATA_1st["user"],
                comment=COR_COMMENT_DATA_1st["comment"],
                pub_date=COR_COMMENT_DATA_1st["pub_date"]
            )
        )

    # すでに場所が登録されている場合
    def test_add_to_sharedplace__if_shared_place_exists(self):
        SharedPlaceCorrectTestData2nd.setUp()
        place = {
            "name": COR_SHA_PLACE_DATA_2nd["name"]
        }
        spv = SharePlaceView()
        # SharedPlaceのオブジェクトが２つのままか確認
        spv.add_to_sharedplace(place)
        self.assertEqual(SharedPlace.objects.count(), 2)

    # まだ場所が登録されていない場合
    def test_add_to_sharedplace__if_shared_place_not_exists(self):
        place = {
            "name": COR_SHA_PLACE_DATA_2nd["name"],
            "linkUrl": COR_SHA_PLACE_DATA_2nd["linkUrl"],
            "imageUrl": COR_SHA_PLACE_DATA_2nd["imageUrl"],
            "extract": COR_SHA_PLACE_DATA_2nd["extract"],
            "latitude": COR_SHA_PLACE_DATA_2nd["latitude"],
            "longtitude": COR_SHA_PLACE_DATA_2nd["longtitude"],
        }
        spv = SharePlaceView()
        spv.add_to_sharedplace(place)

        self.assertTrue(
            SharedPlace.objects.get(
                name=COR_SHA_PLACE_DATA_2nd["name"],
                linkUrl=COR_SHA_PLACE_DATA_2nd["linkUrl"],
                imageUrl=COR_SHA_PLACE_DATA_2nd["imageUrl"],
                extract=COR_SHA_PLACE_DATA_2nd["extract"],
                latitude=COR_SHA_PLACE_DATA_2nd["latitude"],
                longtitude=COR_SHA_PLACE_DATA_2nd["longtitude"],
            )
        )

    def test_connect_comment_place(self):
        CommentCorrectTestData1st.setUp()
        place = {
            "name": COR_SHA_PLACE_DATA_1st["name"]
        }
        com_obj = Comment.objects.get(
            id=COR_COMMENT_DATA_1st["id"])
        spv = SharePlaceView()
        spv.connect_comment_place(place, com_obj)

        self.assertTrue(
            PlaceComment.objects.get(
                share_place=COR_PLC_COMMT_1st["share_place"],
                comment=COR_PLC_COMMT_1st["comment"],
            )
        )


class MockSharedPlaceListView(SharedPlaceListView):
    """
    ユーザー１のセッションを再現するために、
    WSGIのモックを含めたSharedPlaceListViewを定義する
    """
    request = Mock()
    request.session.get = MagicMock(
        return_value=COR_APPUSER_DATA_1st['id'])


class SharedPlaceListViewTestcase(TestCase):
    """
    気になるリストの一覧画面のテスト
    """
    databases = '__all__'

    def setUp(self):
        AppUserCorrectTestData1st.setUp()
        SharedPlaceCorrectTestData1st.setUp()
        CommentCorrectTestData1st.setUp()

    def test_class_variable__is_registered_correctly(self):
        splv = SharedPlaceListView()
        self.assertEqual(
            splv.template_name,
            'travel/shared_place_list.html')

    def test_queryset(self):
        mock_wsgi_session_context()
        splv = MockSharedPlaceListView()
        # モックにする
        expect = 'anything'
        splv.get_place_comment_list = MagicMock(return_value=expect)
        result = splv.queryset()
        self.assertEqual(result, expect)

    @patch(
        'travel.views.SharedPlaceListView.mark_saved_place',
        MagicMock(return_value=True))
    def test_get_place_comment_list(self):
        PlaceCommentCorrectTestData1st.setUp()
        splv = SharedPlaceListView()

        place_comment_list = []
        for obj in SharedPlace.objects.all():
            place_comment = {
                'name': obj.name,
                'linkUrl': obj.linkUrl,
                'imageUrl': obj.imageUrl,
                'extract': obj.extract,
                'latitude': obj.latitude,
                'longtitude': obj.longtitude,
            }
            place_comment["saved"] = True
            comment = PlaceComment.objects.filter(share_place=obj.name)
            place_comment['comment'] = comment
            place_comment_list.append(place_comment)
        expect = place_comment_list
        result = splv.get_place_comment_list('anything')
        for exp_obj, res_obj in zip(expect, result):
            for (k, v), (k2, v2) in zip(exp_obj.items(), res_obj.items()):
                self.assertEqual(k, k2)
                if type(v) is QuerySet:
                    self.assertQuerysetEqual(v, v2, transform=lambda x: x)
                else:
                    self.assertEqual(v, v2)

    def test_get_mark_saved_place__when_place_exist(self):
        PlaceCorrectTestData1st.setUp()
        splv = SharedPlaceListView()

        result = splv.mark_saved_place(
            COR_PLACE_DATA_1st["name"],
            COR_PLACE_DATA_1st["user"]
        )
        self.assertEqual(result, True)

    def test_get_mark_saved_place__when_place_not_exist(self):
        splv = SharedPlaceListView()

        result = splv.mark_saved_place(
            COR_PLACE_DATA_1st["name"],
            COR_PLACE_DATA_1st["user"]
        )
        self.assertEqual(result, False)
