import requests
from collections import OrderedDict


def geo_search(latlon, radius, max_show_num):
    """
    現在地情報と設定を受け取り、場所リストを返す
    """
    places = search_places_from_wiki(latlon, radius, max_show_num)
    # 検索結果が空の場合はNoneを返す
    if places is None:
        return None
    place_list = orgnize_place_data(places)
    return place_list


def search_places_from_wiki(latlon, radius, max_show_num):
    """
    緯度経度と設定をもとにWikipediaAPIで検索する
    """
    session = requests.Session()
    URL = "https://ja.wikipedia.org/w/api.php"
    lat = latlon[0]
    lon = latlon[1]
    params = {
        "action": "query",
        "format": "json",
        "ggscoord": lat + "|" + lon,
        "generator": "geosearch",
        "ggsradius": radius,
        "ggslimit": max_show_num,
        "prop": "pageimages|info",
        "piprop": "thumbnail",
        "pithumbsize": 280,
        "inprop": "url",
    }
    res = session.get(url=URL, params=params)
    data = res.json()
    # 検索結果が空の場合はNoneを返す
    try:
        places = data['query']['pages']
    except KeyError:
        return None
    return places


def orgnize_place_data(places):
    """
    wikipediaで検索した場所情報を整理する
    """
    # pageidの昇順にソートする
    sorted_places = OrderedDict(
        sorted(places.items(), key=lambda x: int(x[0])))
    first_info_list = []
    namelist = []
    for k, v in sorted_places.items():
        place_attr = {}
        place_attr["name"] = str(v['title'])
        place_attr["linkUrl"] = str(v['fullurl'])
        namelist.append(place_attr["name"])
        try:
            place_attr["imageUrl"] = str(v['thumbnail']['source'])
        # 画像がない場合は空にする
        except KeyError:
            place_attr["imageUrl"] = ""
        first_info_list.append(place_attr)

    add_info_list = get_add_info(namelist)
    place_list = []
    for first, addition in zip(first_info_list, add_info_list):
        first.update(addition)
        place_list.append(first)

    return place_list


def get_add_info(namelist):
    """
    追加情報を整理する
    """
    add_info_list = []
    # 要素が２０以上存在する場合は２０ずつのリストに分けて追加情報を取得する
    if len(namelist) > 21:
        devided_namelist = devide_list_by_specific_size(namelist, 20)
        for piece_list in devided_namelist:
            add_info_piece = organize_additional_info(piece_list)
            add_info_list.extend(add_info_piece)
    else:
        add_info_list = organize_additional_info(namelist)

    return add_info_list


def devide_list_by_specific_size(lst, size):
    """
    受け取ったリストを指定したサイズごとのリストに分割する
    """
    multi_list = []
    while len(lst) > size:
        piece = lst[:size]
        multi_list.append(piece)
        lst = lst[size:]
    multi_list.append(lst)
    return multi_list


def search_add_info_from_wiki(page_title):
    """
    記事のタイトルから緯度経度と説明文を取得する
    """
    session = requests.Session()
    URL = "https://ja.wikipedia.org/w/api.php"
    # 複数のタイトルの場合は結合する
    if type(page_title) is list:
        page_title = '|'.join(page_title)

    PARAMS = {
        "action": "query",
        "format": "json",
        "titles": page_title,
        "prop": "coordinates|extracts",
        "exintro": True,
        "explaintext": True,
        "exchars": 128,
    }

    res = session.get(url=URL, params=PARAMS)
    DATA = res.json()
    PAGES = DATA['query']['pages']
    return PAGES


def organize_additional_info(namelist):
    """
    追加情報を整理する
    """
    PAGES = search_add_info_from_wiki(namelist)
    place_info_list = []
    # pageidの昇順にソートする
    sorted_PAGES = OrderedDict(sorted(PAGES.items(), key=lambda x: int(x[0])))
    for k, v in sorted_PAGES.items():
        place_info = {}
        try:
            place_info["latitude"] = str(v['coordinates'][0]['lat'])
            place_info["longtitude"] = str(v['coordinates'][0]['lon'])
        except KeyError:
            # 情報を取得しなおす
            regained_info = search_add_info_from_wiki(v['title'])
            for k, v in regained_info.items():
                place_info["latitude"] = str(v['coordinates'][0]['lat'])
                place_info["longtitude"] = str(v['coordinates'][0]['lon'])
        try:
            place_info["extract"] = str(v['extract'])
        except KeyError:
            place_info["extract"] = ""
        place_info_list.append(place_info)

    return place_info_list
