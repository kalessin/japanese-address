import datetime
import json

import requests
from parsel import Selector


KANJI = {
    "city": "市",
    "ward": "区",
    "district": "郡",
    "town": "町",
    "city_district": "丁目",
}


CITIES_URL = "https://en.wikipedia.org/wiki/List_of_cities_in_Japan"
TOWNS_URL = "https://en.wikipedia.org/wiki/List_of_towns_in_Japan"
WARDS_URL = "https://en.wikipedia.org/wiki/Wards_of_Japan"


def load_cities(endchar):
    response = requests.get(CITIES_URL)
    sel = Selector(text=response.text)
    city_rows = sel.xpath(
        """
        //h2[./span[@id="Cities"]]/following-sibling::table[
            not(preceding-sibling::h2[./span[@id="Dissolved_cities"]])
        ]//tr
    """
    )
    for city in city_rows:
        japanese_name = city.xpath('.//td[2]//span[@lang="ja"]/text()').get() or ""
        english_name = city.xpath(".//td[1]/a/text()").get()
        if japanese_name.endswith(endchar) and english_name:
            yield japanese_name, english_name


def load_towns(endchar):
    response = requests.get(TOWNS_URL)
    sel = Selector(text=response.text)
    town_rows = sel.xpath(
        """
        //h2[./span[@id="Towns"]]/following-sibling::table[
            not(preceding-sibling::h2[./span[@id="See_also"]])
        ]//tr
    """
    )
    for town in town_rows:
        japanese_name = town.xpath('.//td[2]//span[@lang="ja"]/text()').get() or ""
        english_name = town.xpath(".//td[1]/a/text()").get()
        if japanese_name.endswith(endchar) and english_name:
            yield japanese_name, english_name


def load_wards(endchar):
    response = requests.get(WARDS_URL)
    sel = Selector(text=response.text)
    ward_rows = sel.xpath(
        """
        //h2[./span[@id="List_of_wards"]]/following-sibling::table[
            not(preceding-sibling::h2[./span[@id="See_also"]])
        ]//tr
    """
    )
    for ward in ward_rows:
        japanese_name = ward.xpath('.//td[2]//span[@lang="ja"]/text()').get() or ""
        english_name = ward.xpath(".//td[1]/a/text()").get()
        if japanese_name.endswith(endchar) and english_name:
            yield japanese_name, english_name


def generate_dataset():
    update_time = datetime.datetime.now()

    cities_data = {
        japanese_name: english_name
        for japanese_name, english_name in load_cities(KANJI["city"])
    }
    with open("./data/cities.py", "w") as cities_file:
        cities_file.write(f"# Auto-generated file. Last updated: {update_time}\n")
        cities_file.write(
            "JAPANESE_CITIES = {}".format(
                json.dumps(cities_data, ensure_ascii=False, indent=4)
            )
        )

    towns_data = {
        japanese_name: english_name
        for japanese_name, english_name in load_towns(KANJI["town"])
    }
    with open("./data/towns.py", "w") as towns_file:
        towns_file.write(f"# Auto-generated file. Last updated: {update_time}\n")
        towns_file.write(
            "JAPANESE_TOWNS = {}".format(
                json.dumps(towns_data, ensure_ascii=False, indent=4)
            )
        )

    wards_data = {
        japanese_name: english_name
        for japanese_name, english_name in load_wards(KANJI["ward"])
    }
    with open("./data/wards.py", "w") as wards_file:
        wards_file.write(f"# Auto-generated file. Last updated: {update_time}\n")
        wards_file.write(
            "JAPANESE_WARDS = {}".format(
                json.dumps(wards_data, ensure_ascii=False, indent=4)
            )
        )


if __name__ == "__main__":
    generate_dataset()
