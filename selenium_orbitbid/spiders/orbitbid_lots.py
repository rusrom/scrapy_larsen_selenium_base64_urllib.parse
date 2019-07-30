# -*- coding: utf-8 -*-
import scrapy
import re

from base64 import b64decode, b64encode
from urllib.parse import urlsplit, urlunsplit, urljoin, parse_qs, parse_qsl

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from scrapy.selector import Selector

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
from selenium_orbitbid.items import SeleniumOrbitbidItem


class OrbitbidLotsSpider(scrapy.Spider):
    name = 'orbitbid_lots'
    allowed_domains = ['orbitbid.com', 'rangerbid.com', 'repocast.com']
    # start_urls = ['https://bid.orbitbid.com/lots#YXVjdGlvbltpZF09Mzg5OSZhdWN0aW9uW2xvY2F0aW9uXT1hbGwmYXVjdGlvbltzdGF0dXNdPXVwY29taW5nJmF1Y3Rpb25bdHlwZV09YWxsJmxpbWl0PTMwJmxvdFtjYXRlZ29yeV09YWxsJmxvdFtsb2NhdGlvbl09YWxsJmxvdFttaWxlX3JhZGl1c109MjUmcGFnZT0x']
    # start_urls = ['https://bid.rangerbid.com/lots#YXVjdGlvbltpZF09MzgxNSZhdWN0aW9uW2xvY2F0aW9uXT1hbGwmYXVjdGlvbltzdGF0dXNdPXVwY29taW5nJmF1Y3Rpb25bdHlwZV09YWxsJmxpbWl0PTMwJmxvdFtjYXRlZ29yeV09YWxsJmxvdFtsb2NhdGlvbl09YWxsJmxvdFttaWxlX3JhZGl1c109MjUmcGFnZT0x']
    # start_urls = ['https://bid.repocast.com/lots#YXVjdGlvbltpZF09MzgyOSZhdWN0aW9uW3N0YXR1c109dXBjb21pbmcmbG90W2NhdGVnb3J5XT1hbGwmbG90W2tleXdvcmRzXT13bmombG90W2xvY2F0aW9uXT0mbG90W21pbGVfcmFkaXVzXT0yNSZsb3Rbc3RhdHVzXT1hbGw']

    custom_settings = {
        'FEED_EXPORT_FIELDS': ['LotNum', 'Lead', 'Description', 'ClosesOn', 'City', 'State', 'Zip', 'images'],
        'IMAGES_STORE': '**********',
        'AWS_ACCESS_KEY_ID': '**********',
        'AWS_SECRET_ACCESS_KEY': '**********',
        'ITEM_PIPELINES': {
            'selenium_orbitbid.pipelines.LotImagesPipeline': 10,
        },
    }

    # start_urls = [
    #     'https://bid.orbitbid.com/lots/1677060',
    #     'https://bid.orbitbid.com/lots/1677069',
    #     'https://bid.orbitbid.com/lots/1677068',
    #     'https://bid.orbitbid.com/lots/1677067',
    #     'https://bid.orbitbid.com/lots/1677066',
    #     'https://bid.orbitbid.com/lots/1677065',
    #     'https://bid.orbitbid.com/lots/1677064',
    #     'https://bid.orbitbid.com/lots/1677063',
    #     'https://bid.orbitbid.com/lots/1677062',
    #     'https://bid.orbitbid.com/lots/1677061',
    #     'https://bid.orbitbid.com/lots/1677070',
    #     'https://bid.orbitbid.com/lots/1677079',
    #     'https://bid.orbitbid.com/lots/1677078',
    #     'https://bid.orbitbid.com/lots/1677077',
    #     'https://bid.orbitbid.com/lots/1677076',
    #     'https://bid.orbitbid.com/lots/1677075',
    #     'https://bid.orbitbid.com/lots/1677074',
    #     'https://bid.orbitbid.com/lots/1677073',
    #     'https://bid.orbitbid.com/lots/1677072',
    #     'https://bid.orbitbid.com/lots/1677071',
    #     'https://bid.orbitbid.com/lots/1677080',
    #     'https://bid.orbitbid.com/lots/1677089',
    #     'https://bid.orbitbid.com/lots/1677088',
    #     'https://bid.orbitbid.com/lots/1677087',
    #     'https://bid.orbitbid.com/lots/1677086',
    #     'https://bid.orbitbid.com/lots/1677085',
    #     'https://bid.orbitbid.com/lots/1677084',
    #     'https://bid.orbitbid.com/lots/1677083',
    #     'https://bid.orbitbid.com/lots/1677082',
    #     'https://bid.orbitbid.com/lots/1677081',
    #     'https://bid.orbitbid.com/lots/1677090',
    #     'https://bid.orbitbid.com/lots/1677099',
    #     'https://bid.orbitbid.com/lots/1677098',
    #     'https://bid.orbitbid.com/lots/1677097',
    #     'https://bid.orbitbid.com/lots/1677096',
    #     'https://bid.orbitbid.com/lots/1677095',
    #     'https://bid.orbitbid.com/lots/1677094',
    #     'https://bid.orbitbid.com/lots/1677093',
    #     'https://bid.orbitbid.com/lots/1677092',
    #     'https://bid.orbitbid.com/lots/1677091',
    #     'https://bid.orbitbid.com/lots/1677100',
    #     'https://bid.orbitbid.com/lots/1677109',
    #     'https://bid.orbitbid.com/lots/1677108',
    #     'https://bid.orbitbid.com/lots/1677107',
    #     'https://bid.orbitbid.com/lots/1677106',
    #     'https://bid.orbitbid.com/lots/1677105',
    #     'https://bid.orbitbid.com/lots/1677104',
    #     'https://bid.orbitbid.com/lots/1677103',
    #     'https://bid.orbitbid.com/lots/1677102',
    #     'https://bid.orbitbid.com/lots/1677101',
    #     'https://bid.orbitbid.com/lots/1677110',
    #     'https://bid.orbitbid.com/lots/1677117',
    #     'https://bid.orbitbid.com/lots/1677116',
    #     'https://bid.orbitbid.com/lots/1677115',
    #     'https://bid.orbitbid.com/lots/1677114',
    #     'https://bid.orbitbid.com/lots/1677113',
    #     'https://bid.orbitbid.com/lots/1677112',
    #     'https://bid.orbitbid.com/lots/1677111',
    #     'https://bid.orbitbid.com/lots/1677317',
    #     'https://bid.orbitbid.com/lots/1677320'
    # ]

    def decode_fragment(self, fragment):
        fragment_text = fragment.replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '').replace('=', '').strip()
        missing_padding = len(fragment_text) % 4
        if fragment_text != 0:
            fragment_text += '=' * (4 - missing_padding)
        decoded_text = b64decode(fragment_text).decode()
        return decoded_text

    def create_url_with_all_lots(self, url):
        # Parse auction URL
        url_split_result = urlsplit(url)

        # Base64 decode original fragment and decode bytes result to string
        # fragment_decoded = b64decode(url_split_result.fragment).decode()
        fragment_decoded = self.decode_fragment(url_split_result.fragment)

        # Tune query string in order to show 1500 lots on 1 page
        # Encode to bytes for base64 encode processing
        tuned_limit = re.sub(r'limit=\d+', 'limit=1500', fragment_decoded).encode()

        # Base64 encode for changing fragment in SplitResult named tuple
        # Decode from bytes to utf-8 string
        tuned_fragment = b64encode(tuned_limit).decode()

        # Create new SplitResult() with tuned fragment
        tuned_url_data = url_split_result._replace(fragment=tuned_fragment)

        # Create URL from tuned SplitResult()
        tuned_url = urlunsplit(tuned_url_data)

        return tuned_url

    def get_auction_id(self, url):
        # Parse auction URL
        urlsplit_result = urlsplit(url)

        # Base64 decode original fragment and decode bytes result to string
        # fragment_decoded = b64decode(urlsplit_result.fragment).decode()
        fragment_decoded = self.decode_fragment(urlsplit_result.fragment)

        # Querystring dictionary in order to get auction_id from query string
        querystring = dict(parse_qsl(fragment_decoded))

        return querystring['auction[id]']

    def get_domain(self, url):
        url_split_result = urlsplit(url)
        hostname = url_split_result.netloc.lstrip('bid.')
        return hostname

    def __init__(self, url, *args, **kwargs):
        super(OrbitbidLotsSpider, self).__init__(*args, **kwargs)
        self.url = self.create_url_with_all_lots(url)
        self.domain_name = self.get_domain(url)
        self.auction_id = self.get_auction_id(url)

    def start_webdriver(self):
        CHROME_PATH = 'D:\\WebDrivers\\chromedriver.exe'
        driver = webdriver.Chrome(CHROME_PATH)
        driver.set_window_size(1600, 1024)
        return driver

    def get_page_html(self, url):
        driver = self.start_webdriver()
        driver.get(url)
        sleep(5)
        html_code = driver.page_source
        driver.close()
        return html_code

    def start_requests(self):
        html_code = self.get_page_html(self.url)
        response = Selector(text=html_code)
        lots = response.xpath('//div[@class="listing-items"]//div[contains(@class, "item-lot-")]/p[@class="item-lot-number"]/a/@href').getall()
        start_urls = [scrapy.Request(urljoin(self.url, re.sub(r'#.+', '', lot))) for lot in lots]
        return start_urls

    def parse(self, response):
        l = ItemLoader(item=SeleniumOrbitbidItem(), response=response)
        l.default_output_processor = TakeFirst()

        l.add_xpath('LotNum', '//h3//span[contains(text(), "Lot")]/text()')
        l.add_xpath('Lead', '//div[@class="item-title"]/text()')
        l.add_xpath('Description', 'string(//span[@class="item-description"])')
        l.add_xpath('ClosesOn', 'string(//div[label[contains(text(), "Auction Date")]]//following-sibling::div)')
        l.add_xpath('ClosesOn', 'string(//div[label[contains(text(), "Closing At")]]//following-sibling::div)')
        l.add_xpath('City', '//a[@class="btn-location"]/text()')
        l.add_xpath('State', '//a[@class="btn-location"]/text()')
        l.add_xpath('Zip', '//a[@class="btn-location"]/text()')
        l.add_xpath('image_urls', '//script[contains(text(), "media = ")]/text()')
        l.add_value('domain_folder', self.domain_name)
        l.add_value('auction_folder', self.auction_id)

        yield l.load_item()
