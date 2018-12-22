# -*- coding: utf-8 -*-
import logging

from pkg_resources import resource_stream

from parsel import Selector


__version__ = '0.1.2'


logger = logging.getLogger(__name__)


PREFECTURES_DATA = dict([l.decode('utf8').split() for l in resource_stream('japanese_address', 'data/prefs.dat')])
JAPANESE_PREFECTURES = list(PREFECTURES_DATA.keys())


def load_wiki(datafile, endchar):
    sel = Selector(text=resource_stream('japanese_address', datafile).read().decode('utf8'))
    for trow in sel.xpath('//tr'):
        japtext = trow.xpath('.//*[@lang="ja"]/text()').extract()
        if japtext and japtext[0].endswith(endchar):
            engtext = trow.xpath('.//*[@lang="ja"]/ancestor::td/preceding-sibling::td//text()').extract()[-1]
            if engtext:
                yield japtext[0], engtext


CITIES_DATA = dict(load_wiki('data/cities.html', "市"))
WARDS_DATA = dict(load_wiki('data/wards.html', "区"))
TOWNS_DATA = dict(load_wiki('data/towns.html', "町"))


def _parse_prefecture(txt):
    for pref in JAPANESE_PREFECTURES:
        start = txt.find(pref)
        if start >= 0:
            return txt[start:len(pref)].strip()


def _parse_divisor(txt, divisor, dlen):
    start = txt.find(divisor)
    if start >= 0:
        return txt[0:start+dlen].strip()


def _parse_level(div, kanji, parsed):
    dlen = len(kanji)
    if parsed.get('unparsed_right'):
        entity = _parse_divisor(parsed['unparsed_right'], kanji, dlen)
        if entity:
            parsed[div] = entity
            parsed['unparsed_right'] = parsed['unparsed_right'].split(entity, 1)[1].strip()
        elif parsed.get('unparsed_left'):
            entity = _parse_divisor(parsed['unparsed_left'], kanji, dlen)
            if entity:
                parsed[div] = entity
                parsed['unparsed_left'] = parsed['unparsed_left'].split(entity, 1)[1].strip()


def parse(txt):
    """
    >>> parse('北海道 札幌市 中央区北5条西4-7')
    >>> parse('東京都江東区豊洲2丁目4-9')
    """
    parsed = {}
    pref = _parse_prefecture(txt)
    if pref:
        parsed['prefecture'] = pref
        parsed['prefecture_eng'] = PREFECTURES_DATA[pref]
        reml, remr = txt.split(pref, 1)
        if reml:
            parsed['unparsed_left'] = reml.strip()
        if remr:
            parsed['unparsed_right'] = remr.strip()
    else:
        parsed['unparsed_right'] = txt

    _parse_level('city', "市", parsed)
    if 'city' in parsed:
        parsed['city_eng'] = CITIES_DATA[parsed['city']]
    _parse_level('ward', "区", parsed)
    if 'ward' in parsed:
        parsed['ward_eng'] = WARDS_DATA[parsed['ward']]
    _parse_level('district', "郡", parsed)
    _parse_level('town', "町", parsed)
    if 'town' in parsed:
        if parsed['town'] in TOWNS_DATA:
            parsed['town_eng'] = TOWNS_DATA[parsed['town']]
        else:
            logger.warning(f"Town {parsed['town']} not in database")
    _parse_level('city_district', "丁目", parsed)

    return parsed
