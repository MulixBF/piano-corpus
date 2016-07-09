# -*- coding: utf-8 -*-
import scrapy


class MusescoreSpider(scrapy.Spider):
    name = "musescore"
    allowed_domains = ["https://musescore.com"]
    start_urls = (
        'http://www.https://musescore.com/',
    )

    def parse(self, response):
        pass
