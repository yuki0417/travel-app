from uuid import UUID
from json import JSONEncoder

from django.test import TestCase, TransactionTestCase
from django.db.utils import IntegrityError
from django.db.utils import DataError
from accounts.models import AppUser, JSONEncoder_newdefault
from test.unittest.common.test_data import (
    COR_APPUSER_DATA_1st,
    COR_APPUSER_DATA_2nd,
    AppUserCorrectTestData1st,
    AppUserCorrectTestData2nd,
)


class TestJsonEncoder_newdefault(TestCase):
    """
    JsonEncoderのテスト
    """
    def setUp(self):
        AppUserCorrectTestData1st.setUp()

    def test_JSONEncoder_newdefault__with_uuid(self):
        test_uuid = UUID(COR_APPUSER_DATA_1st['id'])

        result = JSONEncoder_newdefault(JSONEncoder_newdefault, test_uuid)
        expect = str(test_uuid)
        self.assertEqual(result, expect)

    def test_JSONEncoder_newdefault__with_no_uuid(self):
        test_obj = 'this_is_not_uuid'

        result = JSONEncoder_newdefault(JSONEncoder_newdefault, test_obj)
        self.assertEqual(result, None)


class TestAppUser(TransactionTestCase):
    """
    ユーザー情報の正常データが登録されるかチェック
    """
    databases = '__all__'

    def setUp(self):
        AppUserCorrectTestData1st.setUp()

    def test_appuser__is_registered_correctly(self):
        appuser_1 = AppUser.objects.get(
            id=COR_APPUSER_DATA_1st["id"])
        self.assertEqual(
            appuser_1.username,
            COR_APPUSER_DATA_1st["username"])
        self.assertEqual(
            appuser_1.password,
            COR_APPUSER_DATA_1st["password"])
        self.assertEqual(
            appuser_1.last_login,
            COR_APPUSER_DATA_1st["last_login"])


class AppUserExceptionTestcase(TransactionTestCase):
    """
    ユーザーグループ情報の制約違反データの例外処理がされているかチェック
    """
    databases = '__all__'

    def setUp(self):
        AppUserCorrectTestData1st.setUp()

    def test_AppUser__max_length_limitation_is_working(self):
        appuser_1 = AppUser.objects.get(
            id=COR_APPUSER_DATA_1st["id"])
        with self.assertRaises(DataError):
            appuser_1.username = ('{}'.format('a' * 21))
            appuser_1.save()
        with self.assertRaises(DataError):
            appuser_1.password = ('{}'.format('a' * 256))
            appuser_1.save()

    def test_AppUser__null_false_is_working(self):
        appuser_1 = AppUser.objects.get(
            id=COR_APPUSER_DATA_1st["id"])
        with self.assertRaises(IntegrityError):
            appuser_1.username = None
            appuser_1.save()
        with self.assertRaises(IntegrityError):
            appuser_1.password = None
            appuser_1.save()
        with self.assertRaises(IntegrityError):
            appuser_1.last_login = None
            appuser_1.save()

    def test_AppUser__id_unique(self):
        with self.assertRaises(IntegrityError):
            AppUserCorrectTestData1st.setUp()

    def test_AppUser__username_unique(self):
        AppUserCorrectTestData2nd.setUp()
        with self.assertRaises(IntegrityError):
            appuser_1 = AppUser.objects.get(
                id=COR_APPUSER_DATA_1st["id"])
            appuser_1.username = COR_APPUSER_DATA_2nd['username']
            appuser_1.save()
