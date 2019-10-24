import requests
from collections import OrderedDict


def geo_search(latlon, radius, max_show_num):

    PLACES = get_places_from_wiki(latlon, radius, max_show_num)
    if PLACES is None:
        return None
    place_list = orgnize_place_data(PLACES)
    return place_list


def get_places_from_wiki(latlon, radius, max_show_num):
    """
    緯度経度から場所の情報を返す
    """
    session = requests.Session()
    URL = "https://ja.wikipedia.org/w/api.php"
    lat = latlon[0]
    lon = latlon[1]

    PARAMS = {
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

    res = session.get(url=URL, params=PARAMS)
    DATA = res.json()

    # 検索結果が空の場合はNoneを返す
    try:
        PLACES = DATA['query']['pages']
    except KeyError:
        return None
    return PLACES


def orgnize_place_data(PLACES):
    # pageidの昇順にソートする
    sorted_PLACES = OrderedDict(
        sorted(PLACES.items(), key=lambda x: int(x[0])))
    first_info_list = []
    namelist = []
    for k, v in sorted_PLACES.items():
        place_attr = {}
        place_attr["name"] = str(v['title'])
        place_attr["linkUrl"] = str(v['fullurl'])
        namelist.append(place_attr["name"])
        try:
            place_attr["imageUrl"] = str(v['thumbnail']['source'])
        except KeyError:
            place_attr["imageUrl"] = ""
        first_info_list.append(place_attr)

    # 要素が２０以上存在する場合は２０ずつのリストに分けて追加情報を取得する
    add_info_list = []
    if len(namelist) > 21:
        devided_namelist = devide_list_by_specific_size(namelist, 20)
        for piece_list in devided_namelist:
            add_info_piece = get_additional_info(piece_list)
            add_info_list.extend(add_info_piece)
    # 緯度経度と説明文を取得し、リストに加える
    else:
        add_info_list = get_additional_info(namelist)
    place_list = []
    for first, addition in zip(first_info_list, add_info_list):
        first.update(addition)
        place_list.append(first)

    return place_list


def devide_list_by_specific_size(arr, size):
    multi_list = []
    while len(arr) > size:
        piece = arr[:size]
        multi_list.append(piece)
        arr = arr[size:]
    multi_list.append(arr)
    return multi_list


def get_add_info_from_wiki(page_title):
    """
    記事のタイトルから緯度経度と説明文を取得する
    """
    session = requests.Session()
    URL = "https://ja.wikipedia.org/w/api.php"
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


def get_additional_info(namelist):
    PAGES = get_add_info_from_wiki(namelist)
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
            regained_info = get_add_info_from_wiki(v['title'])
            for k, v in regained_info.items():
                place_info["latitude"] = str(v['coordinates'][0]['lat'])
                place_info["longtitude"] = str(v['coordinates'][0]['lon'])
        try:
            place_info["extract"] = str(v['extract'])
        except KeyError:
            place_info["extract"] = ""
        place_info_list.append(place_info)

    return place_info_list
