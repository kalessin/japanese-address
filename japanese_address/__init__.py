# -*- coding: utf-8 -*-
import logging
import re

from japanese_address.data import (
    JAPANESE_CITIES,
    JAPANESE_PREFECTURES,
    JAPANESE_TOWNS,
    JAPANESE_WARDS,
)

__version__ = "0.2"


logger = logging.getLogger(__name__)


KANJI = {
    "city": "市",
    "ward": "区",
    "district": "郡",
    "town": "町",
    "city_district": "丁目",
}


def _parse_prefecture(txt):
    for pref in JAPANESE_PREFECTURES:
        start = txt.find(pref)
        if start >= 0:
            return txt[start : start + len(pref)]


def _parse_divisor(txt, divisor, dlen):
    # search for the divisor, skiping the first one (eg. 市川市  => Ichikawa)
    # until the last ocurrence of the divisor (eg. 野々市市 => Nonoichi)
    match = re.search(f"^.+?{divisor}+", txt)
    if match:
        # return the municipality name, without the divisor
        return match.group()


def _parse_level(div, kanji, parsed):
    dlen = len(kanji)
    if parsed.get("unparsed_right"):
        entity = _parse_divisor(parsed["unparsed_right"], kanji, dlen)
        if entity:
            parsed[div] = entity
            parsed["unparsed_right"] = (
                parsed["unparsed_right"].split(entity, 1)[1].strip()
            )
        elif parsed.get("unparsed_left"):
            entity = _parse_divisor(parsed["unparsed_left"], kanji, dlen)
            if entity:
                parsed[div] = entity
                parsed["unparsed_left"] = (
                    parsed["unparsed_left"].split(entity, 1)[1].strip()
                )


def parse(txt):
    """
    >>> parse('北海道 札幌市 中央区北5条西4-7')
    {'prefecture': '北海道', 'prefecture_eng': 'Hokkaido', 'unparsed_right': '北5条西4-7', 'city': '札幌市', 'city_eng': 'Sapporo', 'ward': '中央区', 'ward_eng': 'Chūō'}
    >>> parse('東京都江東区豊洲2丁目4-9')
    {'prefecture': '東京都', 'prefecture_eng': 'Tokyo', 'unparsed_right': '4-9', 'ward': '江東区', 'ward_eng': 'Kōtō', 'city_district': '豊洲2丁目'}
    >>> parse("〒600-8216 京都府京都市下京区烏丸通七条下ル 東塩小路町 721-1")
    {'prefecture': '京都府', 'prefecture_eng': 'Kyoto', 'unparsed_left': '〒600-8216', 'unparsed_right': '721-1', 'city': '京都市', 'city_eng': 'Kyoto', 'ward': '下京区', 'ward_eng': 'Shimogyō', 'town': '烏丸通七条下ル 東塩小路町'}
    """
    parsed = {}
    pref = _parse_prefecture(txt)
    if pref:
        parsed["prefecture"] = pref
        parsed["prefecture_eng"] = JAPANESE_PREFECTURES[pref]
        reml, remr = txt.split(pref, 1)
        if reml:
            parsed["unparsed_left"] = reml.strip()
        if remr:
            parsed["unparsed_right"] = remr.strip()
    else:
        parsed["unparsed_right"] = txt

    _parse_level("city", KANJI["city"], parsed)
    if "city" in parsed and parsed["city"] in JAPANESE_CITIES:
        parsed["city_eng"] = JAPANESE_CITIES[parsed["city"]]

    _parse_level("ward", KANJI["ward"], parsed)
    if "ward" in parsed:
        parsed["ward_eng"] = JAPANESE_WARDS[parsed["ward"]]

    _parse_level("district", KANJI["district"], parsed)

    _parse_level("town", KANJI["town"], parsed)
    if "town" in parsed:
        if parsed["town"] in JAPANESE_TOWNS:
            parsed["town_eng"] = JAPANESE_TOWNS[parsed["town"]]
        else:
            logger.warning(f"Town {parsed['town']} not in database")

    _parse_level("city_district", KANJI["city_district"], parsed)

    return parsed
