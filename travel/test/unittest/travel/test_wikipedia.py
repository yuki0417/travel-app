import requests
from collections import OrderedDict
from unittest.mock import Mock, patch, MagicMock

from django.test import TestCase, TransactionTestCase
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.db.utils import DataError

from travel.wikipedia import (
    geo_search,
    search_places_from_wiki,
    search_add_info_from_wiki,
    make_namelist_and_first_data,
    combine_list_info,
    make_add_info_list,
    devide_list_by_specific_size,
    search_add_info_from_wiki,
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
)


class WikipediaTestcase(TestCase):
    """
    wikipediaのテスト
    """
    # リストが存在する場合
    @patch(
        'travel.wikipedia.search_places_from_wiki',
        MagicMock(return_value=PLACES))
    @patch(
        'travel.wikipedia.make_namelist_and_first_data',
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
