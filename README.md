A Japanese addresses parser

# Install instructions

pip install japanese-address

# Usage

```bash
> from japanese_address import parse
> parse('北海道 札幌市 中央区北5条西4-7')
{'prefecture': '北海道',
 'prefecture_eng': 'Hokkaido',
 'unparsed_right': '北5条西4-7',
 'city': '札幌市',
 'city_eng': 'Sapporo',
 'ward': '中央区',
 'ward_eng': 'Chūō'}
> parse('東京都江東区豊洲2丁目4-9')
{'prefecture': '東京都',
 'prefecture_eng': 'Tokyo',
 'unparsed_right': '4-9',
 'ward': '江東区',
 'ward_eng': 'Kōtō',
 'city_district': '豊洲2丁目'}
```

# Data source

The following Wikipedia pages are used to gather data used to parse Japanese
addresses:

* [List of cities in Japan](https://en.wikipedia.org/wiki/List_of_cities_in_Japan)
* [List of towns in Japan](https://en.wikipedia.org/wiki/List_of_towns_in_Japan)
* [Wards in Japan](https://en.wikipedia.org/wiki/Wards_of_Japan)

To upgrade the data, use the following command:

```bash
$ python dataloader.py
```

If everything goes fine, the files `data/cities.py`, `data/towns.py` and `data/wards.py`
will be updated with the latest content available at the mentioned pages. Commit
them to the repository and create a new release.