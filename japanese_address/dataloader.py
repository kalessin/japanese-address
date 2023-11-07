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
    with open("./data/cities", "w") as cities_file:
        for japanese_name, english_name in load_cities(KANJI["city"]):
            cities_file.write(",".join([japanese_name, english_name]))
            cities_file.write("\n")

    with open("./data/towns", "w") as towns_file:
        for japanese_name, english_name in load_towns(KANJI["town"]):
            towns_file.write(",".join([japanese_name, english_name]))
            towns_file.write("\n")

    with open("./data/wards", "w") as wards_file:
        for japanese_name, english_name in load_wards(KANJI["ward"]):
            wards_file.write(",".join([japanese_name, english_name]))
            wards_file.write("\n")


if __name__ == "__main__":
    generate_dataset()
