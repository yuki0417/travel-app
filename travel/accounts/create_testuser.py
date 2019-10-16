from .models import AppUser


TEST_USER_INFO = {
    "username": "テストユーザー",
    "password": "test",
}


def create_test_user():
    user = AppUser.objects.create(
        username=TEST_USER_INFO["username"],
        password=TEST_USER_INFO["password"],
    )
    return user


def test_user_exists():
    try:
        AppUser.objects.get(
            username=TEST_USER_INFO["username"]
        )
    except AppUser.DoesNotExist:
        return False

    return True
