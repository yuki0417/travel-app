import requests


def geo_search(latlon, radius, max_show_num):
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

    first_info_list = []
    namelist = []
    for k, v in PLACES.items():
        place_attr = {}
        place_attr["name"] = str(v['title'])
        place_attr["linkUrl"] = str(v['fullurl'])
        namelist.append(place_attr["name"])
        try:
            place_attr["imageUrl"] = str(v['thumbnail']['source'])
        except KeyError:
            place_attr["imageUrl"] = ""
        first_info_list.append(place_attr)

    # 緯度経度と説明文を取得し、リストに加える
    add_info_list = get_additional_info(namelist)
    place_list = []
    for first, addition in zip(first_info_list, add_info_list):
        first.update(addition)
        place_list.append(first)

    return place_list


def get_additional_info(namelist):
    """
    記事のタイトルから緯度経度と説明文を取得する
    """
    session = requests.Session()
    URL = "https://ja.wikipedia.org/w/api.php"
    titles = '|'.join(namelist)

    PARAMS = {
        "action": "query",
        "format": "json",
        "titles": titles,
        "prop": "coordinates|extracts",
        "exintro": True,
        "explaintext": True,
        "exchars": 128,
    }

    res = session.get(url=URL, params=PARAMS)
    DATA = res.json()
    PAGES = DATA['query']['pages']
    place_info_list = []
    for k, v in PAGES.items():
        place_info = {}
        # FIXME: 20件越えると緯度経度と説明が取得できない
        # 20件ずつリクエストするなどして対応する？
        try:
            place_info["latitude"] = str(v['coordinates'][0]['lat'])
            place_info["longtitude"] = str(v['coordinates'][0]['lon'])
        except KeyError:
            place_info["latitude"] = ""
            place_info["longtitude"] = ""
        try:
            place_info["extract"] = str(v['extract'])
        except KeyError:
            place_info["extract"] = ""
        place_info_list.append(place_info)
    return place_info_list
