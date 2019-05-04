# -*- coding: utf-8 -*-
_c = {
    'commands': (
        'start',
        'reset'
        'upd',
        'filter',
        'add',
        'find'
    ),
    'apart_categories': (
        'квартира',
    ),
    'commercial_categories': (
        'коммерческая',
    ),
    'house_categories': (
        'дом',
        'дача',
        'коттедж',
        'дом с участком',
        'часть дома',
        'таунхаус',
        'дуплекс'
    ),
    'area_categories': (
        'участок',
    ),
    'prices_ranges': [
        (0, 1000000),
        (1000000, 2500000),
        (2500000, 5000000),
        (5000000, 7500000),
        (7500000, 10000000)
    ],
    'areas_ranges': [
        (0, 30),
        (30, 60),
        (60, 90),
        (90, 150)
    ],
    'html_template': "\
<html>\
<head>\
</head>\
<body>\
{}\
</body>\
</html>",
    'html_img_template': "<img src='{}' />"
}
