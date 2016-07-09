# -*- coding: utf-8 -*-
import scrapy


class KernscoresSpider(scrapy.Spider):
    name = "kernscores"
    allowed_domains = ["http://kern.ccarh.org/"]
    start_urls = (
        'http://www.http://kern.ccarh.org//',
    )

    def parse(self, response):
        pass
