from uuid import UUID
from json import JSONEncoder

from django.test import TestCase, TransactionTestCase
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.db.utils import DataError
from accounts.models import AppUser
from travel.models import (
    Setting,
    Place,
    Comment,
    SharedPlace,
    PlaceComment,
    JSONEncoder_newdefault
)
from test.unittest.common.test_data import (
    COR_APPUSER_DATA_1st,
    COR_APPUSER_DATA_2nd,
    COR_SETTING_DATA_1st,
    COR_SETTING_DATA_2nd,
    COR_PLACE_DATA_1st,
    COR_COMMENT_DATA_1st,
    COR_SHA_PLACE_DATA_1st,
    COR_PLC_COMMT_1st,
    AppUserCorrectTestData1st,
    AppUserCorrectTestData2nd,
    SettingCorrectTestData1st,
    SettingCorrectTestData2nd,
    PlaceCorrectTestData1st,
    CommentCorrectTestData1st,
    SharedPlaceCorrectTestData1st,
    PlaceCommentCorrectTestData1st,
)


class TestJsonEncoder_newdefault(TestCase):
    """
    JsonEncoderのテスト
    """
    def setUp(self):
        AppUserCorrectTestData1st.setUp()
        SettingCorrectTestData1st.setUp()

    def test_JSONEncoder_newdefault__with_uuid(self):
        test_uuid = UUID(COR_APPUSER_DATA_1st['id'])

        result = JSONEncoder_newdefault(JSONEncoder_newdefault, test_uuid)
        expect = str(test_uuid)
        self.assertEqual(result, expect)

    def test_JSONEncoder_newdefault__with_no_uuid(self):
        test_obj = 'this_is_not_uuid'

        result = JSONEncoder_newdefault(JSONEncoder_newdefault, test_obj)
        self.assertEqual(result, None)


class SettingCorrectTestcase(TransactionTestCase):
    """
    設定情報の正常データが登録されるかチェック
    """
    databases = '__all__'

    def setUp(self):
        AppUserCorrectTestData1st.setUp()
        SettingCorrectTestData1st.setUp()

    def test_setting__is_registered_correctly(self):
        test_setting_1 = Setting.objects.get(
            id=COR_SETTING_DATA_1st["id"])
        self.assertEqual(
            str(test_setting_1.user),
            COR_APPUSER_DATA_1st["username"]
            )
        self.assertEqual(
            test_setting_1.name,
            COR_SETTING_DATA_1st["name"])
        self.assertEqual(
            test_setting_1.radius,
            COR_SETTING_DATA_1st["radius"])
        self.assertEqual(
            test_setting_1.max_show_num,
            COR_SETTING_DATA_1st["max_show_num"])


class SettingExceptionTestcase(TransactionTestCase):
    """
    設定情報の制約違反データの例外処理がされているかチェック
    """
    databases = '__all__'

    def setUp(self):
        AppUserCorrectTestData1st.setUp()
        SettingCorrectTestData1st.setUp()

    def test_setting__id_constraints(self):
        with self.assertRaises(IntegrityError):
            SettingCorrectTestData1st.setUp()

    def test_setting__max_length_limitation_is_working(self):
        test_setting_1 = Setting.objects.get(
            id=COR_SETTING_DATA_1st["id"])
        with self.assertRaises(DataError):
            test_setting_1.name = '{}'.format('a' * 21)
            test_setting_1.save()

    def test_setting__null_false_is_working(self):
        test_setting_1 = Setting.objects.get(
            id=COR_SETTING_DATA_1st["id"])
        with self.assertRaises(IntegrityError):
            test_setting_1.id = None
            test_setting_1.save()
        with self.assertRaises(IntegrityError):
            test_setting_1.user = None
            test_setting_1.save()
        with self.assertRaises(IntegrityError):
            test_setting_1.name = None
            test_setting_1.save()
        with self.assertRaises(IntegrityError):
            test_setting_1.radius = None
            test_setting_1.save()
        with self.assertRaises(IntegrityError):
            test_setting_1.max_show_num = None
            test_setting_1.save()


class SettingForeignKeyTestcase(TransactionTestCase):
    """
    設定情報の外部キー制約のテスト
    """
    databases = '__all__'

    def setUp(self):
        AppUserCorrectTestData1st.setUp()
        SettingCorrectTestData1st.setUp()

    def test_setting__foreignkey_on_delete(self):
        appuser_1 = AppUser.objects.get(
            id=COR_APPUSER_DATA_1st["id"])
        appuser_1.delete()
        with self.assertRaises(Setting.DoesNotExist):
            Setting.objects.get(id=COR_SETTING_DATA_1st["id"])


class SettingValidatorsTestcase(TransactionTestCase):
    """
    設定情報のバリデーションのテスト
    """
    databases = '__all__'

    def setUp(self):
        AppUserCorrectTestData1st.setUp()
        SettingCorrectTestData1st.setUp()

    def test_setting__varidator_working(self):
        test_setting_1 = Setting.objects.get(
            id=COR_SETTING_DATA_1st["id"])
        with self.assertRaises(ValidationError):
            test_setting_1.radius = 9
            test_setting_1.full_clean()
        with self.assertRaises(ValidationError):
            test_setting_1.radius = 10001
            test_setting_1.full_clean()
        with self.assertRaises(ValidationError):
            test_setting_1.max_show_num = 501
            test_setting_1.full_clean()


class SettingConstraintTestcase(TransactionTestCase):
    """
    設定情報のカスタム制約のテスト
    """
    databases = '__all__'

    def setUp(self):
        AppUserCorrectTestData1st.setUp()
        AppUserCorrectTestData2nd.setUp()
        SettingCorrectTestData1st.setUp()
        SettingCorrectTestData2nd.setUp()

    def test_setting__user_name_constraints(self):
        appuser_2 = AppUser.objects.get(
            id=COR_APPUSER_DATA_2nd["id"])
        test_setting_1 = Setting.objects.get(
            id=COR_SETTING_DATA_1st["id"])
        with self.assertRaises(ValidationError):
            test_setting_1.user = appuser_2
            test_setting_1.name = COR_SETTING_DATA_2nd['name']
            test_setting_1.full_clean()


class PlaceCorrectTestcase(TransactionTestCase):
    """
    気になる場所リストの正常データが登録されるかチェック
    """
    databases = '__all__'

    def setUp(self):
        AppUserCorrectTestData1st.setUp()
        PlaceCorrectTestData1st.setUp()

    def test_place__is_registered_correctly(self):
        test_place_1 = Place.objects.get(
            id=COR_PLACE_DATA_1st["id"])
        self.assertEqual(
            str(test_place_1.user),
            COR_APPUSER_DATA_1st["username"])
        self.assertEqual(
            test_place_1.name,
            COR_PLACE_DATA_1st["name"])
        self.assertEqual(
            test_place_1.saved_time,
            COR_PLACE_DATA_1st["saved_time"])
        self.assertEqual(
            test_place_1.linkUrl,
            COR_PLACE_DATA_1st["linkUrl"])
        self.assertEqual(
            test_place_1.imageUrl,
            COR_PLACE_DATA_1st["imageUrl"])
        self.assertEqual(
            test_place_1.extract,
            COR_PLACE_DATA_1st["extract"])
        self.assertEqual(
            test_place_1.latitude,
            COR_PLACE_DATA_1st["latitude"])
        self.assertEqual(
            test_place_1.longtitude,
            COR_PLACE_DATA_1st["longtitude"])
        self.assertEqual(
            test_place_1.prefecture,
            COR_PLACE_DATA_1st["prefecture"])
        self.assertEqual(
            test_place_1.city,
            COR_PLACE_DATA_1st["city"])


class PlaceExceptionTestcase(TransactionTestCase):
    """
    気になる場所リストの制約違反したデータの例外処理がされているかチェック
    """
    databases = '__all__'

    def setUp(self):
        AppUserCorrectTestData1st.setUp()
        PlaceCorrectTestData1st.setUp()

    def test_place__max_length_limitation_is_working(self):
        test_place_1 = Place.objects.get(
            id=COR_PLACE_DATA_1st["id"])
        with self.assertRaises(DataError):
            test_place_1.extract = '{}'.format('a' * 257)
            test_place_1.save()
        with self.assertRaises(DataError):
            test_place_1.name = '{}'.format('a' * 257)
            test_place_1.save()
        with self.assertRaises(DataError):
            test_place_1.prefecture = '{}'.format('a' * 5)
            test_place_1.save()
        with self.assertRaises(DataError):
            test_place_1.city = '{}'.format('a' * 10)
            test_place_1.save()

    def test_place__null_false_is_working(self):
        test_place_1 = Place.objects.get(
            id=COR_PLACE_DATA_1st["id"])
        with self.assertRaises(IntegrityError):
            test_place_1.user = None
            test_place_1.save()
        with self.assertRaises(IntegrityError):
            test_place_1.name = None
            test_place_1.save()
        with self.assertRaises(IntegrityError):
            test_place_1.saved_time = None
            test_place_1.save()


class PlaceForeignKeyTestcase(TransactionTestCase):
    """
    気になる場所リストの外部キー制約のテスト
    """
    databases = '__all__'

    def setUp(self):
        AppUserCorrectTestData1st.setUp()
        PlaceCorrectTestData1st.setUp()

    def test_place__foreignkey_on_delete(self):
        appuser_1 = AppUser.objects.get(
            id=COR_APPUSER_DATA_1st["id"])
        appuser_1.delete()
        with self.assertRaises(Place.DoesNotExist):
            Place.objects.get(id=COR_PLACE_DATA_1st["id"])


class PlaceStrTestcase(TransactionTestCase):
    """
    気になる場所リストの__str__のテスト
    """
    databases = '__all__'

    def setUp(self):
        AppUserCorrectTestData1st.setUp()
        PlaceCorrectTestData1st.setUp()

    def test_place_str_(self):
        test_place_1 = Place.objects.get(
            id=COR_PLACE_DATA_1st["id"])

        result = str(test_place_1)
        expect = COR_PLACE_DATA_1st["name"]
        self.assertEqual(expect, result)


class CommentTestcase(TransactionTestCase):
    """
    コメントの正常データが登録されるかチェック
    """
    databases = '__all__'

    def setUp(self):
        AppUserCorrectTestData1st.setUp()
        CommentCorrectTestData1st.setUp()

    def test_comment__is_registered_correctly(self):
        test_comment_1 = Comment.objects.get(
            id=COR_COMMENT_DATA_1st["id"])
        self.assertEqual(
            str(test_comment_1.user),
            COR_APPUSER_DATA_1st["username"])
        self.assertEqual(
            test_comment_1.comment,
            COR_COMMENT_DATA_1st["comment"])
        self.assertEqual(
            test_comment_1.pub_date,
            COR_COMMENT_DATA_1st["pub_date"])


class CommentExceptionTestcase(TransactionTestCase):
    """
    コメントの制約違反したデータの例外処理がされているかチェック
    """
    databases = '__all__'

    def setUp(self):
        AppUserCorrectTestData1st.setUp()
        CommentCorrectTestData1st.setUp()

    def test_comment__null_false_is_working(self):
        test_comment_1 = Comment.objects.get(
            id=COR_COMMENT_DATA_1st["id"])
        with self.assertRaises(IntegrityError):
            test_comment_1.user = None
            test_comment_1.save()


class SharedPlaceCorrectTestcase(TransactionTestCase):
    """
    シェアされた場所の正常データが登録されるかチェック
    """
    databases = '__all__'

    def setUp(self):
        AppUserCorrectTestData1st.setUp()
        SharedPlaceCorrectTestData1st.setUp()

    def test_sha_place__is_registered_correctly(self):
        test_sha_place_1 = SharedPlace.objects.get(
            id=COR_SHA_PLACE_DATA_1st["id"])
        self.assertEqual(
            test_sha_place_1.name,
            COR_SHA_PLACE_DATA_1st["name"])
        self.assertEqual(
            test_sha_place_1.linkUrl,
            COR_SHA_PLACE_DATA_1st["linkUrl"])
        self.assertEqual(
            test_sha_place_1.imageUrl,
            COR_SHA_PLACE_DATA_1st["imageUrl"])
        self.assertEqual(
            test_sha_place_1.extract,
            COR_SHA_PLACE_DATA_1st["extract"])
        self.assertEqual(
            test_sha_place_1.latitude,
            COR_SHA_PLACE_DATA_1st["latitude"])
        self.assertEqual(
            test_sha_place_1.longtitude,
            COR_SHA_PLACE_DATA_1st["longtitude"])
        self.assertEqual(
            test_sha_place_1.prefecture,
            COR_SHA_PLACE_DATA_1st["prefecture"])
        self.assertEqual(
            test_sha_place_1.city,
            COR_SHA_PLACE_DATA_1st["city"])


class SharedPlaceExceptionTestcase(TransactionTestCase):
    """
    シェアされた場所の制約違反したデータの例外処理がされているかチェック
    """
    databases = '__all__'

    def setUp(self):
        AppUserCorrectTestData1st.setUp()
        SharedPlaceCorrectTestData1st.setUp()

    def test_sha_place__max_length_limitation_is_working(self):
        test_sha_place_1 = SharedPlace.objects.get(
            id=COR_SHA_PLACE_DATA_1st["id"])
        with self.assertRaises(DataError):
            test_sha_place_1.extract = '{}'.format('a' * 257)
            test_sha_place_1.save()
        with self.assertRaises(DataError):
            test_sha_place_1.name = '{}'.format('a' * 257)
            test_sha_place_1.save()
        with self.assertRaises(DataError):
            test_sha_place_1.prefecture = '{}'.format('a' * 5)
            test_sha_place_1.save()
        with self.assertRaises(DataError):
            test_sha_place_1.city = '{}'.format('a' * 10)
            test_sha_place_1.save()

    def test_sha_place__null_false_is_working(self):
        test_sha_place_1 = SharedPlace.objects.get(
            id=COR_SHA_PLACE_DATA_1st["id"])
        with self.assertRaises(IntegrityError):
            test_sha_place_1.name = None
            test_sha_place_1.save()


class PlaceCommentCorrectTestcase(TransactionTestCase):
    """
    気になる場所リストの正常データが登録されるかチェック
    """
    databases = '__all__'

    def setUp(self):
        AppUserCorrectTestData1st.setUp()
        CommentCorrectTestData1st.setUp()
        PlaceCommentCorrectTestData1st.setUp()

    def test_plc_commt__is_registered_correctly(self):
        test_plc_commt_1 = PlaceComment.objects.get(
            id=COR_PLC_COMMT_1st["id"])
        self.assertEqual(
            test_plc_commt_1.share_place,
            COR_PLC_COMMT_1st["share_place"])
        self.assertEqual(
            str(test_plc_commt_1.comment.id),
            COR_COMMENT_DATA_1st["id"])


class PlaceCommentExceptionTestcase(TransactionTestCase):
    """
    気になる場所リストの制約違反したデータの例外処理がされているかチェック
    """
    databases = '__all__'

    def setUp(self):
        AppUserCorrectTestData1st.setUp()
        CommentCorrectTestData1st.setUp()
        PlaceCommentCorrectTestData1st.setUp()

    def test_plc_commt__max_length_limitation_is_working(self):
        test_plc_commt_1 = PlaceComment.objects.get(
            id=COR_PLC_COMMT_1st["id"])
        with self.assertRaises(DataError):
            test_plc_commt_1.share_place = '{}'.format('a' * 256)
            test_plc_commt_1.save()

    def test_plc_commt__null_false_is_working(self):
        test_plc_commt_1 = PlaceComment.objects.get(
            id=COR_PLC_COMMT_1st["id"])
        with self.assertRaises(IntegrityError):
            test_plc_commt_1.comment = None
            test_plc_commt_1.save()


class PlaceCommentForeignKeyTestcase(TransactionTestCase):
    """
    気になる場所リストの外部キー制約のテスト
    """
    databases = '__all__'

    def setUp(self):
        AppUserCorrectTestData1st.setUp()
        CommentCorrectTestData1st.setUp()
        PlaceCommentCorrectTestData1st.setUp()

    def test_plc_commt__foreignkey_on_delete(self):
        comment_1 = Comment.objects.get(
            id=COR_COMMENT_DATA_1st["id"])
        comment_1.delete()
        with self.assertRaises(PlaceComment.DoesNotExist):
            PlaceComment.objects.get(id=COR_PLC_COMMT_1st["id"])
