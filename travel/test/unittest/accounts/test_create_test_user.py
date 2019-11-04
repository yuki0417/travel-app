from django.test import TestCase

from accounts.models import AppUser
from accounts.create_testuser import (
    TEST_USER_INFO,
    create_test_user,
    is_test_user_exists,
)


class CreateTestUserTestcase(TestCase):
    """
    アカウント作成の画面のテスト
    """
    databases = '__all__'

    def test_TEST_USER_INFO(self):
        expect = {
            "username": "テストユーザー",
            "password": "test",
        }
        self.assertEqual(TEST_USER_INFO, expect)

    def test_create_test_user(self):
        self.assertEqual(
            create_test_user(),
            AppUser.objects.get(
                username=TEST_USER_INFO["username"],
                password=TEST_USER_INFO["password"],
            )
        )

    def test_is_test_user_exists__when_test_user_exists(self):
        create_test_user()
        self.assertEqual(is_test_user_exists(), True)

    def test_is_test_user_exists__when_test_user_not_exists(self):
        self.assertEqual(is_test_user_exists(), False)
