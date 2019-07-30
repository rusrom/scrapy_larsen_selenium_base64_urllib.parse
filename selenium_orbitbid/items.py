# -*- coding: utf-8 -*-
import scrapy
import re

from w3lib.html import replace_escape_chars, replace_entities
from scrapy.loader.processors import Identity, MapCompose, Join, Compose


def get_city(val):
    city = val.split(',')[1]
    city = city.strip()
    return city


def get_state(val):
    state = val.split(',')[-1]
    state = re.sub(r'\s+\d.+', '', state)
    # state = re.sub('[^A-Z]', '', state)
    state = re.search(r'[A-Z]+', state)
    state = state.group() if state else 'Cant find state'
    return state


def get_zip(val):
    zip_code = val.split(',')[-1]
    zip_code = re.search(r'\d+', zip_code)
    zip_code = zip_code.group() if zip_code else 'Cant find ZIP'
    return zip_code


class SeleniumOrbitbidItem(scrapy.Item):
    LotNum = scrapy.Field(
        input_processor=MapCompose(
            lambda val: val.replace('Lot ', '').strip(),
        ),
    )
    Lead = scrapy.Field()
    Description = scrapy.Field()
    ClosesOn = scrapy.Field(
        input_processor=MapCompose(
            lambda val: val.strip(),
        ),
        output_processor=Join(' at ')
    )
    City = scrapy.Field(
        input_processor=MapCompose(
            get_city,
        )
    )
    State = scrapy.Field(
        input_processor=MapCompose(
            get_state,
        )
    )
    Zip = scrapy.Field(
        input_processor=MapCompose(
            get_zip,
        )
    )
    image_urls = scrapy.Field(
        input_processor=Compose(
            lambda val: re.findall(r'{"src":"([^"]+)', val[0]),
            MapCompose(
                lambda val: 'https:' + val,
            )
        ),
        output_processor=Identity(),
    )
    images = scrapy.Field()
    domain_folder = scrapy.Field()
    auction_folder = scrapy.Field()
