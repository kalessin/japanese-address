A japanese addresses parser

# installation

pip install japanese-address

# Usage

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
