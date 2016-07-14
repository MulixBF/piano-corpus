# -*- coding: utf-8 -*-
import scrapy
from src.items import Composition


class AllMusicSpider(scrapy.Spider):
    name = 'allmusic'
    allowed_domains = ['www.allmusic.com']

    urls = {
        'beethoven': u'http://www.allmusic.com/artist/ludwig-van-beethoven-mn0000536126',
        'mozart': u'http://www.allmusic.com/artist/wolfgang-amadeus-mozart-mn0000026350',
        'bach': u'http://www.allmusic.com/artist/johann-sebastian-bach-mn0000075140',
        #'bartok': u'http://www.allmusic.com/artist/b%C3%A9la-bart%C3%B3k-mn0000534880',
        #'chopin': u'http://www.allmusic.com/artist/fr%C3%A9d%C3%A9ric-chopin-mn0000066824',
        'debussy': u'http://www.allmusic.com/artist/claude-debussy-mn0000768781',
        'stravinsky': u'http://www.allmusic.com/artist/igor-stravinsky-mn0000364751',
        'berlioz': u'http://www.allmusic.com/artist/hector-berlioz-mn0001436021',
    }

    def start_requests(self):
        for composer, page_url in self.urls.items():
            yield scrapy.Request(page_url, self.parse, meta={composer: composer})

    def parse(self, response):
        info_links = response.x('//a[contains(@href, "format=info")]')

        for link in info_links:
            url = link.xpath('@href').extract_first()
            yield scrapy.Request(url, self._parse_info_page)
