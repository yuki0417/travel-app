import copy
from datetime import datetime
import pytz

from django.contrib.auth.hashers import make_password

from accounts.models import AppUser
from django.contrib.auth.models import User
from django.test import TestCase
from travel.models import (
    Setting,
    Place,
    Comment,
    SharedPlace,
    PlaceComment,
    JSONEncoder_newdefault
)


####################################################################

# テストに用いる関数の定義

def list_difference(list1, list2):
    """
    2つのリストの差分を求め、元の順番のまま出力する関数
    """
    result = copy.deepcopy(list1)
    for value in list2:
        if value in result:
            result.remove(value)

    return result


def teardown_data():
    try:
        AppUser.objects.all().delete()
    except AppUser.DoesNotExist:
        pass
    try:
        Setting.objects.all().delete()
    except Setting.DoesNotExist:
        pass
    try:
        Place.objects.all().delete()
    except Place.DoesNotExist:
        pass
    try:
        Comment.objects.all().delete()
    except Comment.DoesNotExist:
        pass
    try:
        SharedPlace.objects.all().delete()
    except SharedPlace.DoesNotExist:
        pass
    try:
        PlaceComment.objects.all().delete()
    except PlaceComment.DoesNotExist:
        pass


####################################################################

# テストに用いるデータの定義はここに記述する

# NOTE: デフォルト値を定義したものの使用方法（自動生成の時刻以外）
# 例：　"radius": Setting._meta.get_field('radius').default


# 時間の定数

TEST_DATETIME_1 = pytz.utc.localize(datetime(2019, 1, 25, 23, 59, 59))
TEST_DATETIME_2 = pytz.utc.localize(datetime(2019, 12, 31, 23, 59, 59))
TEST_DATETIME_3 = pytz.utc.localize(datetime(2019, 8, 30, 23, 59, 59))


# ユーザー情報の定数

APPUSER_ID_1 = '60717df1-8d82-4b66-8acc-10258b890a15'
APPUSER_ID_2 = '7f7cccd4-5d0b-4b37-9a0d-3f7e61fcd87f'
APPUSER_ID_3 = '7d943474-3c2e-4391-af33-edbca1e0fe5c'

APPUSER_NAME_1 = 'ユニットテストユーザー1'
APPUSER_NAME_2 = 'ユニットテストユーザー2'
APPUSER_NAME_3 = 'ユニットテストユーザー3'

APPUSER_PW_1 = 'password_1'
APPUSER_PW_2 = 'password_2'
APPUSER_PW_3 = 'password_3'

APPUSER_LOGIN_1 = TEST_DATETIME_1
APPUSER_LOGIN_2 = TEST_DATETIME_2
APPUSER_LOGIN_3 = TEST_DATETIME_3

UNDEFINED_ID = ''
NOEXIST_ID = 'something should be inside'


# 設定情報の定数

SETTING_ID_1 = '7a7ea4ff-7819-4288-af40-d432c5b6b8c6'
SETTING_ID_2 = '2565c4e5-9a8e-495b-8936-ffc20a16a041'
SETTING_ID_3 = '1c1a226e-014a-4e18-aa6b-ed0bd078ee7e'

SETTING_USER_1 = APPUSER_ID_1
SETTING_USER_2 = APPUSER_ID_2
SETTING_USER_3 = APPUSER_ID_3

SETTING_NAME_1 = '設定1'
SETTING_NAME_2 = '設定2'
SETTING_NAME_3 = '設定3'

SETTING_RADIUS_1 = 500
SETTING_RADIUS_2 = 1000
SETTING_RADIUS_3 = 1500

SETTING_MAXSHNUM_1 = 5
SETTING_MAXSHNUM_2 = 8
SETTING_MAXSHNUM_3 = 10


# 気になる場所リストの定数

PLACE_ID_1 = 'fef26e95-d2d0-4ea9-8324-49d5187996f9'
PLACE_ID_2 = 'db2ff188-fab3-47ac-9a2e-cbeac2f7f3ee'
PLACE_ID_3 = '6024b662-698d-486a-8bc5-5813a045f767'

PLACE_USER_1 = APPUSER_ID_1
PLACE_USER_2 = APPUSER_ID_2
PLACE_USER_3 = APPUSER_ID_3

PLACE_NAME_1 = '場所1'
PLACE_NAME_2 = '場所2'
PLACE_NAME_3 = '場所3'

PLACE_SAVED_TIME_1 = TEST_DATETIME_1
PLACE_SAVED_TIME_2 = TEST_DATETIME_2
PLACE_SAVED_TIME_3 = TEST_DATETIME_3

PLACE_LINKURL_1 = (
    'https://ja.wikipedia.org/wiki/%E6%98%AF%E6%94%BF%E9%A7%85'
)
PLACE_LINKURL_2 = (
    'https://ja.wikipedia.org/wiki/'
    'JRA%E7%AB%B6%E9%A6%AC%E5%8D%9A%E7%89%A9%E9%A4%A8'
)
PLACE_LINKURL_3 = (
    'https://ja.wikipedia.org/wiki/'
    '%E5%A4%9A%E6%91%A9%E5%B7%9D%E7%AB%B6%E8%89%87%E5%A0%B4'
)
PLACE_IMGURL_1 = (
    'https://upload.wikimedia.org/wikipedia/commons/thumb/7/76/'
    'Koremasa_station.JPG/280px-Koremasa_station.JPG'
)
PLACE_IMGURL_2 = (
    'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/'
    'JRA-RACING_MUSEUM.jpg/280px-JRA-RACING_MUSEUM.jpg'
)
PLACE_IMGURL_3 = (
    'https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/'
    'Tamagawa-kyotei-01.jpg/280px-Tamagawa-kyotei-01.jpg'
)

PLACE_EXTRACT_1 = '場所1の説明です'
PLACE_EXTRACT_2 = '場所2の説明です'
PLACE_EXTRACT_3 = '場所3の説明です'

PLACE_LATITUDE_1 = 35.66833333
PLACE_LATITUDE_2 = 35.66222222
PLACE_LATITUDE_3 = 35.65633333

PLACE_LONGTITUDE_1 = 139.48611111
PLACE_LONGTITUDE_2 = 139.48555556
PLACE_LONGTITUDE_3 = 139.48877778

PLACE_PREFECTURE_1 = "東京都"
PLACE_PREFECTURE_2 = "神奈川県"
PLACE_PREFECTURE_3 = "和歌山県"

PLACE_CITY_1 = "新宿区"
PLACE_CITY_2 = "横浜市"
PLACE_CITY_3 = "和歌山市"


# コメントの定数

COMMENT_ID_1 = 'fff11e95-d2d0-4ea9-8324-49d5187996f9'
COMMENT_ID_2 = 'aaa11e95-d2d0-4ea9-8324-49d5187996f9'
COMMENT_ID_3 = 'bbb11e95-d2d0-4ea9-8324-49d5187996f9'

COMMENT_USER_1 = APPUSER_ID_1
COMMENT_USER_2 = APPUSER_ID_2
COMMENT_USER_3 = APPUSER_ID_3

COMMENT_COMMENT_1 = "すばらしい"
COMMENT_COMMENT_2 = "きれい"
COMMENT_COMMENT_3 = "うつくしい"

COMMENT_PUB_DATE_1 = TEST_DATETIME_1
COMMENT_PUB_DATE_2 = TEST_DATETIME_1
COMMENT_PUB_DATE_3 = TEST_DATETIME_1


# シェアされた場所の定数

SHA_PLACE_ID_1 = 'fff11e95-d2d0-4ea9-8324-121212121212'
SHA_PLACE_ID_2 = 'aaa11e95-d2d0-4ea9-8324-222222222222'
SHA_PLACE_ID_3 = 'bbb11e95-d2d0-4ea9-8324-333333333333'

SHA_PLACE_NAME_1 = PLACE_NAME_1
SHA_PLACE_NAME_2 = PLACE_NAME_2
SHA_PLACE_NAME_3 = PLACE_NAME_3

SHA_PLACE_LINKURL_1 = PLACE_LINKURL_1
SHA_PLACE_LINKURL_2 = PLACE_LINKURL_2
SHA_PLACE_LINKURL_3 = PLACE_LINKURL_3

SHA_PLACE_IMGURL_1 = PLACE_IMGURL_1
SHA_PLACE_IMGURL_2 = PLACE_IMGURL_2
SHA_PLACE_IMGURL_3 = PLACE_IMGURL_3

SHA_PLACE_EXTRACT_1 = PLACE_EXTRACT_1
SHA_PLACE_EXTRACT_2 = PLACE_EXTRACT_2
SHA_PLACE_EXTRACT_3 = PLACE_EXTRACT_3

SHA_PLACE_LATITUDE_1 = PLACE_LATITUDE_1
SHA_PLACE_LATITUDE_2 = PLACE_LATITUDE_2
SHA_PLACE_LATITUDE_3 = PLACE_LATITUDE_3

SHA_PLACE_LONGTITUDE_1 = PLACE_LONGTITUDE_1
SHA_PLACE_LONGTITUDE_2 = PLACE_LONGTITUDE_2
SHA_PLACE_LONGTITUDE_3 = PLACE_LONGTITUDE_3

SHA_PLACE_PREFECTURE_1 = PLACE_PREFECTURE_1
SHA_PLACE_PREFECTURE_2 = PLACE_PREFECTURE_2
SHA_PLACE_PREFECTURE_3 = PLACE_PREFECTURE_3

SHA_PLACE_CITY_1 = PLACE_CITY_1
SHA_PLACE_CITY_2 = PLACE_CITY_2
SHA_PLACE_CITY_3 = PLACE_CITY_3


# シェアされた場所とコメントを紐づけるテーブルの定数

PLC_COMMT_ID_1 = 'fff11e95-d2d0-4ea9-8324-343433434344'
PLC_COMMT_ID_2 = 'aaa11e95-d2d0-4ea9-8324-544333343434'
PLC_COMMT_ID_3 = 'bbb11e95-d2d0-4ea9-8324-555555555555'

PLC_COMMT_SH_PLC_1 = SHA_PLACE_NAME_1
PLC_COMMT_SH_PLC_2 = SHA_PLACE_NAME_2
PLC_COMMT_SH_PLC_3 = SHA_PLACE_NAME_3

PLC_COMMT_COMMENT_1 = COMMENT_ID_1
PLC_COMMT_COMMENT_2 = COMMENT_ID_2
PLC_COMMT_COMMENT_3 = COMMENT_ID_3


####################################################################

# 管理者ユーザー情報の定義

ADMIN_USER = {
    "username": "traveladminsite_user",
    "email": "traveladminsite_user@test.com",
    "password": "test",
}


# ユーザー情報の定義

COR_APPUSER_DATA_1st = {
    "id": APPUSER_ID_1,
    "username": APPUSER_NAME_1,
    "password": APPUSER_PW_1,
    "last_login": APPUSER_LOGIN_1,
}

COR_APPUSER_DATA_2nd = {
    "id": APPUSER_ID_2,
    "username": APPUSER_NAME_2,
    "password": APPUSER_PW_2,
    "last_login": APPUSER_LOGIN_2,
}

COR_APPUSER_DATA_3rd = {
    "id": APPUSER_ID_3,
    "username": APPUSER_NAME_3,
    "password": APPUSER_PW_3,
    "last_login": APPUSER_LOGIN_3,
}

# 設定情報の定義

COR_SETTING_DATA_1st = {
    "id": SETTING_ID_1,
    "user": SETTING_USER_1,
    "name": SETTING_NAME_1,
    "radius": SETTING_RADIUS_1,
    "max_show_num": SETTING_MAXSHNUM_1,
}

COR_SETTING_DATA_2nd = {
    "id": SETTING_ID_2,
    "user": SETTING_USER_2,
    "name": SETTING_NAME_2,
    "radius": SETTING_RADIUS_2,
    "max_show_num": SETTING_MAXSHNUM_2,
}

COR_SETTING_DATA_3rd = {
    "id": SETTING_ID_3,
    "user": SETTING_USER_3,
    "name": SETTING_NAME_3,
    "radius": SETTING_RADIUS_3,
    "max_show_num": SETTING_MAXSHNUM_3,
}


# 気になる場所リストの定義

COR_PLACE_DATA_1st = {
    "id": PLACE_ID_1,
    "user": PLACE_USER_1,
    "name": PLACE_NAME_1,
    "saved_time": PLACE_SAVED_TIME_1,
    "linkUrl": PLACE_LINKURL_1,
    "imageUrl": PLACE_IMGURL_1,
    "extract": PLACE_EXTRACT_1,
    "latitude": PLACE_LATITUDE_1,
    "longtitude": PLACE_LONGTITUDE_1,
    "prefecture": PLACE_PREFECTURE_1,
    "city": PLACE_CITY_1,
}

COR_PLACE_DATA_2nd = {
    "id": PLACE_ID_2,
    "user": PLACE_USER_2,
    "name": PLACE_NAME_2,
    "saved_time": PLACE_SAVED_TIME_2,
    "linkUrl": PLACE_LINKURL_2,
    "imageUrl": PLACE_IMGURL_2,
    "extract": PLACE_EXTRACT_2,
    "latitude": PLACE_LATITUDE_2,
    "longtitude": PLACE_LONGTITUDE_2,
    "prefecture": PLACE_PREFECTURE_2,
    "city": PLACE_CITY_2,
}

COR_PLACE_DATA_3rd = {
    "id": PLACE_ID_3,
    "user": PLACE_USER_3,
    "name": PLACE_NAME_3,
    "saved_time": PLACE_SAVED_TIME_3,
    "linkUrl": PLACE_LINKURL_3,
    "imageUrl": PLACE_IMGURL_3,
    "extract": PLACE_EXTRACT_3,
    "latitude": PLACE_LATITUDE_3,
    "longtitude": PLACE_LONGTITUDE_2,
    "prefecture": PLACE_PREFECTURE_3,
    "city": PLACE_CITY_3,
}


# コメントの定義

COR_COMMENT_DATA_1st = {
    "id": COMMENT_ID_1,
    "user": COMMENT_USER_1,
    "comment": COMMENT_COMMENT_1,
    "pub_date": COMMENT_PUB_DATE_1,
}

COR_COMMENT_DATA_2nd = {
    "id": COMMENT_ID_2,
    "user": COMMENT_USER_2,
    "comment": COMMENT_COMMENT_2,
    "pub_date": COMMENT_PUB_DATE_2,
}

COR_COMMENT_DATA_3rd = {
    "id": COMMENT_ID_3,
    "user": COMMENT_USER_3,
    "comment": COMMENT_COMMENT_3,
    "pub_date": COMMENT_PUB_DATE_3,
}


# シェアされた場所の定義

COR_SHA_PLACE_DATA_1st = {
    "id": SHA_PLACE_ID_1,
    "name": SHA_PLACE_NAME_1,
    "linkUrl": SHA_PLACE_LINKURL_1,
    "imageUrl": SHA_PLACE_IMGURL_1,
    "extract": SHA_PLACE_EXTRACT_1,
    "latitude": SHA_PLACE_LATITUDE_1,
    "longtitude": SHA_PLACE_LONGTITUDE_1,
    "prefecture": SHA_PLACE_PREFECTURE_1,
    "city": SHA_PLACE_CITY_1,
}

COR_SHA_PLACE_DATA_2nd = {
    "id": SHA_PLACE_ID_2,
    "name": SHA_PLACE_NAME_2,
    "linkUrl": SHA_PLACE_LINKURL_2,
    "imageUrl": SHA_PLACE_IMGURL_2,
    "extract": SHA_PLACE_EXTRACT_2,
    "latitude": SHA_PLACE_LATITUDE_2,
    "longtitude": SHA_PLACE_LONGTITUDE_2,
    "prefecture": SHA_PLACE_PREFECTURE_2,
    "city": SHA_PLACE_CITY_2,
}

COR_SHA_PLACE_DATA_3rd = {
    "id": SHA_PLACE_ID_3,
    "name": SHA_PLACE_NAME_3,
    "linkUrl": SHA_PLACE_LINKURL_3,
    "imageUrl": SHA_PLACE_IMGURL_3,
    "extract": SHA_PLACE_EXTRACT_3,
    "latitude": SHA_PLACE_LATITUDE_3,
    "longtitude": SHA_PLACE_LONGTITUDE_3,
    "prefecture": SHA_PLACE_PREFECTURE_3,
    "city": SHA_PLACE_CITY_3,
}

# シェアされた場所の定義

COR_PLC_COMMT_1st = {
    "id": PLC_COMMT_ID_1,
    "share_place": PLC_COMMT_SH_PLC_1,
    "comment": PLC_COMMT_COMMENT_1,
}

COR_PLC_COMMT_2nd = {
    "id": PLC_COMMT_ID_2,
    "share_place": PLC_COMMT_SH_PLC_2,
    "comment": PLC_COMMT_COMMENT_2,
}

COR_PLC_COMMT_3rd = {
    "id": PLC_COMMT_ID_3,
    "share_place": PLC_COMMT_SH_PLC_3,
    "comment": PLC_COMMT_COMMENT_3,
}


# テストデータのセットアップ用のプログラム
# 呼び出し時は引数を指定せず呼び出す
# 例：　AdminUserTestData.setUp()


class AdminUserTestData(TestCase):
    """
    管理者ユーザー情報のセットアップ
    """
    databases = '__all__'

    @classmethod
    def setUp(cls):
        User.objects.create_superuser(
            username=ADMIN_USER["username"],
            email=ADMIN_USER["email"],
            password=ADMIN_USER["password"]
        )


class AppUserCorrectTestData1st(TestCase):
    """
    ユーザー情報の正常データのセットアップその１
    """
    databases = '__all__'

    @classmethod
    def setUp(cls):
        AppUser.objects.create(
            id=COR_APPUSER_DATA_1st["id"],
            username=COR_APPUSER_DATA_1st["username"],
            password=COR_APPUSER_DATA_1st["password"],
            last_login=COR_APPUSER_DATA_1st["last_login"],
        )


class AppUserCorrectTestData2nd(TestCase):
    """
    ユーザー情報の正常データのセットアップその２
    """
    databases = '__all__'

    @classmethod
    def setUp(cls):
        AppUser.objects.create(
            id=COR_APPUSER_DATA_2nd["id"],
            username=COR_APPUSER_DATA_2nd["username"],
            password=COR_APPUSER_DATA_2nd["password"],
            last_login=COR_APPUSER_DATA_2nd["last_login"],
        )


class AppUserEncPasswordTestData1st(TestCase):
    """
    ユーザー情報の正常データのセットアップその２
    """
    databases = '__all__'

    @classmethod
    def setUp(cls):
        AppUser.objects.create(
            id=COR_APPUSER_DATA_1st["id"],
            username=COR_APPUSER_DATA_1st["username"],
            password=make_password(COR_APPUSER_DATA_1st["password"]),
            last_login=COR_APPUSER_DATA_1st["last_login"],
        )


class SettingCorrectTestData1st(TestCase):
    """
    設定の正常データのセットアップその１
    """
    databases = '__all__'

    @classmethod
    def setUp(cls):
        Setting.objects.create(
            id=COR_SETTING_DATA_1st["id"],
            user=AppUser.objects.get(
                id=COR_SETTING_DATA_1st["user"]),
            name=COR_SETTING_DATA_1st["name"],
            radius=COR_SETTING_DATA_1st["radius"],
            max_show_num=COR_SETTING_DATA_1st["max_show_num"],
        )


class SettingCorrectTestData2ndUser1st(TestCase):
    """
    設定の正常データのセットアップその１
    ユーザーは上記と同一で、設定はその２を使う
    """
    databases = '__all__'

    @classmethod
    def setUp(cls):
        Setting.objects.create(
            id=COR_SETTING_DATA_2nd["id"],
            user=AppUser.objects.get(
                id=COR_SETTING_DATA_1st["user"]),
            name=COR_SETTING_DATA_2nd["name"],
            radius=COR_SETTING_DATA_2nd["radius"],
            max_show_num=COR_SETTING_DATA_2nd["max_show_num"],
        )


class SettingCorrectTestData2nd(TestCase):
    """
    設定の正常データのセットアップその２
    """
    databases = '__all__'

    @classmethod
    def setUp(cls):
        Setting.objects.create(
            id=COR_SETTING_DATA_2nd["id"],
            user=AppUser.objects.get(
                id=COR_SETTING_DATA_2nd["user"]),
            name=COR_SETTING_DATA_2nd["name"],
            radius=COR_SETTING_DATA_2nd["radius"],
            max_show_num=COR_SETTING_DATA_2nd["max_show_num"],
        )


class PlaceCorrectTestData1st(TestCase):
    """
    気になる場所リストの正常データのセットアップその１
    """
    databases = '__all__'

    @classmethod
    def setUp(cls):
        Place.objects.create(
            id=COR_PLACE_DATA_1st["id"],
            user=AppUser.objects.get(
                id=COR_PLACE_DATA_1st["user"]),
            name=COR_PLACE_DATA_1st["name"],
            saved_time=COR_PLACE_DATA_1st["saved_time"],
            linkUrl=COR_PLACE_DATA_1st["linkUrl"],
            imageUrl=COR_PLACE_DATA_1st["imageUrl"],
            extract=COR_PLACE_DATA_1st["extract"],
            latitude=COR_PLACE_DATA_1st["latitude"],
            longtitude=COR_PLACE_DATA_1st["longtitude"],
            prefecture=COR_PLACE_DATA_1st["prefecture"],
            city=COR_PLACE_DATA_1st["city"],
        )


class PlaceCorrectTestData2nd(TestCase):
    """
    気になる場所リストの正常データのセットアップその２
    """
    databases = '__all__'

    @classmethod
    def setUp(cls):
        Place.objects.create(
            id=COR_PLACE_DATA_2nd["id"],
            user=AppUser.objects.get(
                id=COR_PLACE_DATA_2nd["user"]),
            name=COR_PLACE_DATA_2nd["name"],
            saved_time=COR_PLACE_DATA_2nd["saved_time"],
            linkUrl=COR_PLACE_DATA_2nd["linkUrl"],
            imageUrl=COR_PLACE_DATA_2nd["imageUrl"],
            extract=COR_PLACE_DATA_2nd["extract"],
            latitude=COR_PLACE_DATA_2nd["latitude"],
            longtitude=COR_PLACE_DATA_2nd["longtitude"],
            prefecture=COR_PLACE_DATA_2nd["prefecture"],
            city=COR_PLACE_DATA_2nd["city"],
        )


class CommentCorrectTestData1st(TestCase):
    """
    コメントの正常データのセットアップその１
    """
    databases = '__all__'

    @classmethod
    def setUp(cls):
        Comment.objects.create(
            id=COR_COMMENT_DATA_1st["id"],
            user=AppUser.objects.get(
                id=COR_COMMENT_DATA_1st["user"]),
            comment=COR_COMMENT_DATA_1st["comment"],
            pub_date=COR_COMMENT_DATA_1st["pub_date"],
        )


class CommentCorrectTestData2nd(TestCase):
    """
    コメントの正常データのセットアップその２
    """
    databases = '__all__'

    @classmethod
    def setUp(cls):
        Comment.objects.create(
            id=COR_COMMENT_DATA_2nd["id"],
            user=AppUser.objects.get(
                id=COR_COMMENT_DATA_2nd["user"]),
            comment=COR_COMMENT_DATA_2nd["comment"],
            pub_date=COR_COMMENT_DATA_2nd["pub_date"],
        )


class CommentCorrectTestData3rd(TestCase):
    """
    コメントの正常データのセットアップその３
    """
    databases = '__all__'

    @classmethod
    def setUp(cls):
        Comment.objects.create(
            id=COR_COMMENT_DATA_3rd["id"],
            user=AppUser.objects.get(
                id=COR_COMMENT_DATA_3rd["user"]),
            comment=COR_COMMENT_DATA_3rd["comment"],
            pub_date=COR_COMMENT_DATA_3rd["pub_date"],
        )


class SharedPlaceCorrectTestData1st(TestCase):
    """
    シェアされた場所の正常データのセットアップその１
    """
    databases = '__all__'

    @classmethod
    def setUp(cls):
        SharedPlace.objects.create(
            id=COR_SHA_PLACE_DATA_1st["id"],
            name=COR_SHA_PLACE_DATA_1st["name"],
            linkUrl=COR_SHA_PLACE_DATA_1st["linkUrl"],
            imageUrl=COR_SHA_PLACE_DATA_1st["imageUrl"],
            extract=COR_SHA_PLACE_DATA_1st["extract"],
            latitude=COR_SHA_PLACE_DATA_1st["latitude"],
            longtitude=COR_SHA_PLACE_DATA_1st["longtitude"],
            prefecture=COR_SHA_PLACE_DATA_1st["prefecture"],
            city=COR_SHA_PLACE_DATA_1st["city"],
        )


class SharedPlaceCorrectTestData2nd(TestCase):
    """
    シェアされた場所の正常データのセットアップその２
    """
    databases = '__all__'

    @classmethod
    def setUp(cls):
        SharedPlace.objects.create(
            id=COR_SHA_PLACE_DATA_2nd["id"],
            name=COR_SHA_PLACE_DATA_2nd["name"],
            linkUrl=COR_SHA_PLACE_DATA_2nd["linkUrl"],
            imageUrl=COR_SHA_PLACE_DATA_2nd["imageUrl"],
            extract=COR_SHA_PLACE_DATA_2nd["extract"],
            latitude=COR_SHA_PLACE_DATA_2nd["latitude"],
            longtitude=COR_SHA_PLACE_DATA_2nd["longtitude"],
            prefecture=COR_SHA_PLACE_DATA_2nd["prefecture"],
            city=COR_SHA_PLACE_DATA_2nd["city"],
        )


class SharedPlaceCorrectTestData3rd(TestCase):
    """
    シェアされた場所の正常データのセットアップその３
    """
    databases = '__all__'

    @classmethod
    def setUp(cls):
        SharedPlace.objects.create(
            id=COR_SHA_PLACE_DATA_3rd["id"],
            name=COR_SHA_PLACE_DATA_3rd["name"],
            linkUrl=COR_SHA_PLACE_DATA_3rd["linkUrl"],
            imageUrl=COR_SHA_PLACE_DATA_3rd["imageUrl"],
            extract=COR_SHA_PLACE_DATA_3rd["extract"],
            latitude=COR_SHA_PLACE_DATA_3rd["latitude"],
            longtitude=COR_SHA_PLACE_DATA_3rd["longtitude"],
            prefecture=COR_SHA_PLACE_DATA_3rd["prefecture"],
            city=COR_SHA_PLACE_DATA_3rd["city"],
        )


class PlaceCommentCorrectTestData1st(TestCase):
    """
    シェアされた場所とコメントを紐づけるテーブルの正常データのセットアップその１
    """
    databases = '__all__'

    @classmethod
    def setUp(cls):
        PlaceComment.objects.create(
            id=COR_PLC_COMMT_1st["id"],
            share_place=COR_PLC_COMMT_1st["share_place"],
            comment=Comment.objects.get(
                id=COR_PLC_COMMT_1st["comment"]),
        )


class PlaceCommentCorrectTestData2nd(TestCase):
    """
    シェアされた場所とコメントを紐づけるテーブルの正常データのセットアップその２
    """
    databases = '__all__'

    @classmethod
    def setUp(cls):
        PlaceComment.objects.create(
            id=COR_PLC_COMMT_2nd["id"],
            share_place=COR_PLC_COMMT_2nd["share_place"],
            comment=Comment.objects.get(
                id=COR_PLACE_DATA_2nd["comment"]),
        )


class PlaceCommentCorrectTestData3rd(TestCase):
    """
    シェアされた場所とコメントを紐づけるテーブルの正常データのセットアップその３
    """
    databases = '__all__'

    @classmethod
    def setUp(cls):
        PlaceComment.objects.create(
            id=COR_PLC_COMMT_3rd["id"],
            share_place=COR_PLC_COMMT_3rd["share_place"],
            comment=Comment.objects.get(
                id=COR_PLC_COMMT_3rd["comment"]),
        )


#######################################################################
# modeladmin用のテストデータ
# NOTICE: " *_FIELDS_* " で定義されたmodelのフィールドの指定順序は、
# テスト時の評価に影響を与えるので変えないこと


USERGROUPINFO_FIELDS_ALL = (
    'group_name',
    'eff_date',
    'exp_date',
    'version',
    'remarks',
    'max_capacity',
    'cur_capacity',
    'delete_flag',
    'key_code',
    'max_ws_count',
    'max_user_count',
)

USERGROUPINFO_FIELDS_READONLY = (
    'gid',
    'delete_flag',
    'key_code',
    'cur_capacity',
)

USERGROUPINFO_FIELDS_EDITABLE = list_difference(
    list(USERGROUPINFO_FIELDS_ALL),
    list(USERGROUPINFO_FIELDS_READONLY),
)

USERINFO_FIELDS_ALL = (
    'login_id',
    'user_name',
    'gid',
    'wid',
    'remarks',
    'temp_password',
    'priv',
    'delete_flag',
    'max_capacity',
    'cur_capacity',
    'photo_priv',
    'max_import_size',
    'max_addr_import_count',
    'max_shape_import_count',
    'max_stats_import_count',
    'api_key',
    'reg_date',
    'last_login',
    'system_code',
    'api_key_update_date',
    'enc_password',
    'sys_flag',
    'thematic_public_flag',
    'stats_category',
    'access_denied_count',
    'last_password_change_date',
    'exp_date',
    'stats_pattern_id',
)

USERINFO_FIELDS_READONLY = (
    'usr_seq_id',
    'api_key',
    'delete_flag',
    'system_code',
    'api_key_update_date',
    'thematic_public_flag',
    'stats_category',
    'access_denied_count',
    'last_password_change_date',
    'cur_capacity',
    'last_login',
    'sys_flag',
    'photo_priv',
)

USERINFO_FIELDS_EDITABLE = list_difference(
    list(USERINFO_FIELDS_ALL),
    list(USERINFO_FIELDS_READONLY),
)

WORKSPACEINFO_FIELDS_ALL = (
    'wid',
    'gid',
    'name',
    'keycode',
)

WORKSPACEINFO_FIELDS_READONLY = (
    'wid',
    'keycode',
)

WORKSPACEINFO_FIELDS_EDITABLE = list_difference(
    list(WORKSPACEINFO_FIELDS_ALL),
    list(WORKSPACEINFO_FIELDS_READONLY),
)

OPERARIONLOG_FIELDS_ALL = (
    'operation_date',
    'user_id',
    'operation',
    'detail1',
    'detail2',
    'detail3',
    'user_kind',
    'device_kind',
)

OPERARIONLOG_FIELDS_READONLY = OPERARIONLOG_FIELDS_ALL
OPERARIONLOG_FIELDS_EDITABLE = ()

#################################################################
# wikipediaAPIのテストデータ


def wiki_page_response(pages):
    wiki_page = {
        "batchcomplete": "",
        "query": {
            "pages": pages
        }
    }
    return wiki_page


PLACE_TITLE_1 = '場所タイトル1'
PLACE_TITLE_2 = '場所タイトル2'
PLACE_TITLE_3 = '場所タイトル3'
PAGEID_1 = 111111
PAGEID_2 = 222222
PAGEID_3 = 333333
PAGE_EXTRACT_1 = '場所の説明１'
PAGE_EXTRACT_2 = '場所の説明２'
PAGE_EXTRACT_3 = '場所の説明３'
PAGE_LATITUDE_1 = 35.111111
PAGE_LATITUDE_2 = 35.222222
PAGE_LATITUDE_3 = 35.333333
PAGE_LONGTUDE_1 = 139.111111
PAGE_LONGTUDE_2 = 139.222222
PAGE_LONGTUDE_3 = 139.333333
LINKURL_1 = 'https://ja.wikipedia.org/wiki/linkUrl_1'
LINKURL_2 = 'https://ja.wikipedia.org/wiki/linkUrl_2'
IMAGE_URL_1 = 'https://upload.wikimedia.org/wikipedia/image_1.jpg'
IMAGE_URL_2 = 'https://upload.wikimedia.org/wikipedia/image_2.jpg'

PLACES = {
    PAGEID_1: {
        'pageid': PAGEID_1,
        'ns': 0,
        'title': PLACE_TITLE_1,
        'index': -1,
        'thumbnail': {
            'source': IMAGE_URL_1,
            'width': 280,
            'height': 158
        },
        'contentmodel': 'wikitext',
        'pagelanguage': 'ja',
        'pagelanguagehtmlcode': 'ja',
        'pagelanguagedir': 'ltr',
        'touched': '2019-10-03T03:31:15Z',
        'lastrevid': 74480464,
        'length': 14137,
        'fullurl': LINKURL_1,
        'editurl': 'https://ja.wikipedia.org/wiki/editurl_1',
        'canonicalurl': 'https://ja.wikipedia.org/wiki/canonicalurl_1',
    },
    PAGEID_2: {
        'pageid': PAGEID_2,
        'ns': 0,
        'title': PLACE_TITLE_2,
        'index': -1,
        'thumbnail': {
            'source': IMAGE_URL_2,
            'width': 280,
            'height': 158
        },
        'contentmodel': 'wikitext',
        'pagelanguage': 'ja',
        'pagelanguagehtmlcode': 'ja',
        'pagelanguagedir': 'ltr',
        'touched': '2019-10-03T03:31:15Z',
        'lastrevid': 74480464,
        'length': 14137,
        'fullurl': LINKURL_2,
        'editurl': 'https://ja.wikipedia.org/wiki/editurl_2',
        'canonicalurl': 'https://ja.wikipedia.org/wiki/canonicalurl_2',
    }
}

PLACES_NO_IMAGE = {
    PAGEID_1: {
        'pageid': PAGEID_1,
        'ns': 0,
        'title': PLACE_TITLE_1,
        'index': -1,
        'contentmodel': 'wikitext',
        'pagelanguage': 'ja',
        'pagelanguagehtmlcode': 'ja',
        'pagelanguagedir': 'ltr',
        'touched': '2019-10-03T03:31:15Z',
        'lastrevid': 74480464,
        'length': 14137,
        'fullurl': LINKURL_1,
        'editurl': 'https://ja.wikipedia.org/wiki/editurl_1',
        'canonicalurl': 'https://ja.wikipedia.org/wiki/canonicalurl_1',
    },
    PAGEID_2: {
        'pageid': PAGEID_2,
        'ns': 0,
        'title': PLACE_TITLE_2,
        'index': -1,
        'contentmodel': 'wikitext',
        'pagelanguage': 'ja',
        'pagelanguagehtmlcode': 'ja',
        'pagelanguagedir': 'ltr',
        'touched': '2019-10-03T03:31:15Z',
        'lastrevid': 74480464,
        'length': 14137,
        'fullurl': LINKURL_2,
        'editurl': 'https://ja.wikipedia.org/wiki/editurl_2',
        'canonicalurl': 'https://ja.wikipedia.org/wiki/canonicalurl_2',
    }
}

WIKI_PLACE_LIST = [
    {
        'name': PLACE_TITLE_1,
        'linkUrl': LINKURL_1,
        'imageUrl': IMAGE_URL_1,
        'latitude': str(PAGE_LATITUDE_1),
        'longtitude': str(PAGE_LONGTUDE_1),
        'extract': PAGE_EXTRACT_1
    },
    {
        'name': PLACE_TITLE_2,
        'linkUrl': LINKURL_2,
        'imageUrl': IMAGE_URL_2,
        'latitude': str(PAGE_LATITUDE_2),
        'longtitude': str(PAGE_LONGTUDE_2),
        'extract': PAGE_EXTRACT_2
    }
]

WIKI_DATA = {
    'batchcomplete': '',
    'query': {
        'pages': PLACES
    }
}

WIKI_DATA_NONE = {'batchcomplete': ''}

PAGE_TITLES_LIST = [PLACE_TITLE_1, PLACE_TITLE_2]
PAGE_TITLE_SOLO = '場所'

PAGE_1 = {
    PAGEID_1: {
        "pageid": PAGEID_1,
        "ns": 0,
        "title": PLACE_TITLE_1,
        "coordinates": [
            {
                "lat": PAGE_LATITUDE_1,
                "lon": PAGE_LONGTUDE_1,
                "primary": "",
                "globe": "earth"
            }
        ],
        "extract": PAGE_EXTRACT_1
    },
}

PAGE_2 = {
    PAGEID_2: {
        "pageid": PAGEID_2,
        "ns": 0,
        "title": PLACE_TITLE_2,
        "coordinates": [
            {
                "lat": PAGE_LATITUDE_2,
                "lon": PAGE_LONGTUDE_2,
                "primary": "",
                "globe": "earth"
            }
        ],
        "extract": PAGE_EXTRACT_2
    }
}

PAGE_3 = {
    PAGEID_3: {
        "pageid": PAGEID_3,
        "ns": 0,
        "title": PLACE_TITLE_3,
        "coordinates": [
            {
                "lat": PAGE_LATITUDE_3,
                "lon": PAGE_LONGTUDE_3,
                "primary": "",
                "globe": "earth"
            }
        ],
        "extract": PAGE_EXTRACT_3
    }
}

PAGES = copy.deepcopy(PAGE_1)
PAGES.update(PAGE_2)

WIKI_PAGE_1 = wiki_page_response(PAGE_1)
WIKI_PAGE_2 = wiki_page_response(PAGE_2)
WIKI_PAGE_3 = wiki_page_response(PAGE_3)

WIKI_PAGES = wiki_page_response(PAGES)

PAGE_SOLO = PAGE_3
WIKI_PAGE_SOLO = WIKI_PAGE_3

ADD_INFO_LIST_TWO = [
    {
        "latitude": str(PAGE_LATITUDE_1),
        "longtitude": str(PAGE_LONGTUDE_1),
        "extract": PAGE_EXTRACT_1
    },
    {
        "latitude": str(PAGE_LATITUDE_2),
        "longtitude": str(PAGE_LONGTUDE_2),
        "extract": PAGE_EXTRACT_2
    }
]

ADD_INFO_LIST_THREE = [
    {
        "latitude": str(PAGE_LATITUDE_1),
        "longtitude": str(PAGE_LONGTUDE_1),
        "extract": PAGE_EXTRACT_1
    },
    {
        "latitude": str(PAGE_LATITUDE_2),
        "longtitude": str(PAGE_LONGTUDE_2),
        "extract": PAGE_EXTRACT_2
    },
    {
        "latitude": str(PAGE_LATITUDE_3),
        "longtitude": str(PAGE_LONGTUDE_3),
        "extract": PAGE_EXTRACT_3
    }
]

PAGES_NO_LATLON = {
    PAGEID_1: {
        "pageid": PAGEID_1,
        "ns": 0,
        "title": PLACE_TITLE_1,
        "coordinates": [
            {
                "primary": "",
                "globe": "earth"
            }
        ],
        "extract": PAGE_EXTRACT_1
    },
    PAGEID_2: {
        "pageid": PAGEID_2,
        "ns": 0,
        "title": PLACE_TITLE_2,
        "coordinates": [
            {
                "primary": "",
                "globe": "earth"
            }
        ],
        "extract": PAGE_EXTRACT_2
    },
    PAGEID_3: {
        "pageid": PAGEID_3,
        "ns": 0,
        "title": PLACE_TITLE_3,
        "coordinates": [
            {
                "primary": "",
                "globe": "earth"
            }
        ],
        "extract": PAGE_EXTRACT_3
    }
}

WIKI_PAGES_NO_LATLON = wiki_page_response(PAGES_NO_LATLON)

LIST_1 = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10
]
LIST_2 = [
    11, 12, 13, 14, 15, 16, 17, 18, 19, 20
]
LIST_3 = [
    21, 22, 22, 24, 25, 26, 27, 28, 29, 30
]

LIST = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
    11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
    21, 22, 22, 24, 25, 26, 27, 28, 29, 30
]

LIST_20 = copy.deepcopy(LIST_1)
LIST_20.extend(LIST_2)

FIRST_INFO_LIST = [
    {
        'name': PLACE_TITLE_1,
        'linkUrl': LINKURL_1,
        'imageUrl': IMAGE_URL_1,
    },
    {
        'name': PLACE_TITLE_2,
        'linkUrl': LINKURL_2,
        'imageUrl': IMAGE_URL_2,
    }
]

FIRST_INFO_LIST_NO_IMAGE = [
    {
        'name': PLACE_TITLE_1,
        'linkUrl': LINKURL_1,
        'imageUrl': '',
    },
    {
        'name': PLACE_TITLE_2,
        'linkUrl': LINKURL_2,
        'imageUrl': '',
    }
]

#################################################################
# travel.viewsのテストデータ


WIKI_PLACE_LIST_SAVED_EXIST = [
    {
        'name': PLACE_NAME_1,  # NOTE: モデル保存済みの名前にしておく
        'linkUrl': LINKURL_1,
        'imageUrl': IMAGE_URL_1,
        'latitude': str(PAGE_LATITUDE_1),
        'longtitude': str(PAGE_LONGTUDE_1),
        'extract': PAGE_EXTRACT_1
    },
    {
        'name': PLACE_TITLE_2,
        'linkUrl': LINKURL_2,
        'imageUrl': IMAGE_URL_2,
        'latitude': str(PAGE_LATITUDE_2),
        'longtitude': str(PAGE_LONGTUDE_2),
        'extract': PAGE_EXTRACT_2
    }
]

YOUR_LOCATION = ['35.1234567', '139.123456']

PLACE_LIST_SAVED_MARKED = [
    {
        'name': PLACE_NAME_1,
        'linkUrl': LINKURL_1,
        'imageUrl': IMAGE_URL_1,
        'latitude': str(PAGE_LATITUDE_1),
        'longtitude': str(PAGE_LONGTUDE_1),
        'extract': PAGE_EXTRACT_1,
        'saved': True
    },
    {
        'name': PLACE_TITLE_2,
        'linkUrl': LINKURL_2,
        'imageUrl': IMAGE_URL_2,
        'latitude': str(PAGE_LATITUDE_2),
        'longtitude': str(PAGE_LONGTUDE_2),
        'extract': PAGE_EXTRACT_2,
        'saved': False
    }
]
