import requests
import copy
from unittest.mock import patch, MagicMock

from django.test import TestCase

from travel.wikipedia import (
    geo_search,
    search_places_from_wiki,
    search_add_info_from_wiki,
    make_namelist_and_first_data,
    combine_list_info,
    make_add_info_list,
    devide_list_by_specific_size,
    organize_additional_info
)
from test.unittest.common.test_data import (
    PAGES,
    PLACES,
    WIKI_PLACE_LIST,
    WIKI_DATA,
    WIKI_DATA_NONE,
    PAGE_TITLES_LIST,
    WIKI_PAGES,
    PAGE_TITLE_SOLO,
    WIKI_PAGE_SOLO,
    PAGE_SOLO,
    ADD_INFO_LIST_TWO,
    WIKI_PAGES_NO_LATLON,
    WIKI_PAGE_1,
    WIKI_PAGE_2,
    WIKI_PAGE_3,
    ADD_INFO_LIST_THREE,
    LIST,
    LIST_1,
    LIST_2,
    LIST_3,
    LIST_20,
    FIRST_INFO_LIST,
    PLACES_NO_IMAGE,
    FIRST_INFO_LIST_NO_IMAGE
)


class GeoSearchTestcase(TestCase):
    """
    geo_searchのテスト
    """
    # リストが存在する場合
    @patch(
        'travel.wikipedia.search_places_from_wiki',
        MagicMock(return_value=PLACES))
    @patch(
        'travel.wikipedia.make_namelist_and_first_data',
        MagicMock(return_value=['anything', 'anything']))
    @patch(
        'travel.wikipedia.combine_list_info',
        MagicMock(return_value=WIKI_PLACE_LIST))
    def test_geo_search__with_list(self):
        latlon = ['35.55555', '139.55555']
        radius = 5000
        max_show_num = 30
        result = geo_search(latlon, radius, max_show_num)
        self.assertEqual(result, WIKI_PLACE_LIST)

    # リストが存在しない場合
    @patch(
        'travel.wikipedia.search_places_from_wiki',
        MagicMock(return_value=None))
    def test_geo_search__with_none(self):
        latlon = ['35.55555', '139.55555']
        radius = 5000
        max_show_num = 30
        result = geo_search(latlon, radius, max_show_num)
        self.assertEqual(result, None)


class SearchPlacesFromWikiTestcase(TestCase):
    """
    search_places_from_wikiのテスト
    """
    # 検索結果が存在する場合
    @patch.object(requests.Session, 'get')
    def test_search_places_from_wiki__with_list(self, mock_get):
        mock_get.return_value.json.return_value = WIKI_DATA
        latlon = ['35.55555', '139.55555']
        radius = 5000
        max_show_num = 30
        result = search_places_from_wiki(latlon, radius, max_show_num)
        self.assertEqual(result, PLACES)

    # 検索結果が存在しない場合
    @patch.object(requests.Session, 'get')
    def test_search_places_from_wiki__with_none(self, mock_get):
        mock_get.return_value.json.return_value = WIKI_DATA_NONE
        latlon = ['35.55555', '139.55555']
        radius = 5000
        max_show_num = 30
        result = search_places_from_wiki(latlon, radius, max_show_num)
        self.assertEqual(result, None)


class SearchAddInfoFromWikiTestcase(TestCase):
    """
    search_add_info_from_wikiのテスト
    """
    # リストで検索する場合
    @patch.object(requests.Session, 'get')
    def test_search_add_info_from_wiki__with_list(self, mock_get):
        mock_get.return_value.json.return_value = WIKI_PAGES
        result = search_add_info_from_wiki(PAGE_TITLES_LIST)
        self.assertEqual(result, PAGES)

    # 一つのタイトルのみで検索する場合
    @patch.object(requests.Session, 'get')
    def test_search_add_info_from_wiki__with_solo(self, mock_get):
        mock_get.return_value.json.return_value = WIKI_PAGE_SOLO
        result = search_add_info_from_wiki(PAGE_TITLE_SOLO)
        self.assertEqual(result, PAGE_SOLO)


class OrganizeAdditionalInfoTestcase(TestCase):
    """
    organize_additional_infoのテスト
    """
    # 通常の場合
    @patch.object(requests.Session, 'get')
    def test_organize_additional_info__with_no_error(self, mock_get):
        mock_get.return_value.json.return_value = WIKI_PAGES
        result = organize_additional_info(PAGE_TITLES_LIST)
        self.assertEqual(result, ADD_INFO_LIST_TWO)

    # 複数回呼び出す場合
    @patch.object(requests.Session, 'get')
    def test_organize_additional_info__with_key_error(self, mock_get):
        # 計4回search_add_info_from_wikiを呼び出す
        mock_get.return_value.json.side_effect = [
            WIKI_PAGES_NO_LATLON,
            WIKI_PAGE_1,
            WIKI_PAGE_2,
            WIKI_PAGE_3
        ]
        result = organize_additional_info(PAGE_TITLES_LIST)
        self.assertEqual(result, ADD_INFO_LIST_THREE)


class DevideListBySpecificTestcase(TestCase):
    """
    devide_list_by_specific_sizeのテスト
    """
    def test_devide_list_by_specific_size(self):
        result = devide_list_by_specific_size(LIST, 10)
        self.assertEqual(result, [LIST_1, LIST_2, LIST_3])


class MakeAddInfoListTestcase(TestCase):
    """
    make_add_info_listのテスト
    """
    # リストに２１以上要素がある場合
    @patch(
        'travel.wikipedia.devide_list_by_specific_size',
        MagicMock(return_value=[LIST_1, LIST_2, LIST_3]))
    @patch(
        'travel.wikipedia.organize_additional_info',
        MagicMock(side_effect=[LIST_1, LIST_2, LIST_3]))
    def test_make_add_info_list__with_length50(self):
        result = make_add_info_list(LIST)
        self.assertEqual(result, LIST)

    # リストに２０以下の要素がある場合
    @patch(
        'travel.wikipedia.organize_additional_info',
        MagicMock(return_value=LIST_20))
    def test_make_add_info_list__with_length10(self):
        result = make_add_info_list(LIST_20)
        # import pdb;pdb.set_trace()
        self.assertEqual(result, LIST_20)


class CombineListInfoTestcase(TestCase):
    """
    combine_list_infoのテスト
    """
    @patch(
        'travel.wikipedia.make_add_info_list',
        MagicMock(return_value=ADD_INFO_LIST_TWO))
    def test_combine_list_info(self):
        # 他のテストデータに影響するので深いコピーする
        FIRST_INFO_LIST_TMP = copy.deepcopy(FIRST_INFO_LIST)
        result = combine_list_info('anything', FIRST_INFO_LIST_TMP)
        self.assertEqual(result, WIKI_PLACE_LIST)


class MakeNameListAndFirstDataTestcase(TestCase):
    """
    wikipediaのテスト
    """
    # 画像がある場合
    def test_make_namelist_and_first_data__with_imageurl(self):
        result = make_namelist_and_first_data(PLACES)
        self.assertEqual(result, (PAGE_TITLES_LIST, FIRST_INFO_LIST))

    # 画像がない場合
    def test_make_namelist_and_first_data__with_no_imageurl(self):
        result = make_namelist_and_first_data(PLACES_NO_IMAGE)
        self.assertEqual(result, (PAGE_TITLES_LIST, FIRST_INFO_LIST_NO_IMAGE))
