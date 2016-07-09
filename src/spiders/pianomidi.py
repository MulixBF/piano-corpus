# -*- coding: utf-8 -*-
import scrapy


class PianomidiSpider(scrapy.Spider):
    name = "pianomidi"
    allowed_domains = ["www.piano-midi.de"]
    start_urls = (
        'http://www.www.piano-midi.de/',
    )

    def parse(self, response):
        pass
