# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy


class Composition(scrapy.Item):
    file_urls = scrapy.Field()
    files = scrapy.Field()
    name = scrapy.Field()
    genre = scrapy.Field()
    composer = scrapy.Field()
    instruments = scrapy.Field()
    tags = scrapy.Field()
    type = scrapy.Field()
    year = scrapy.Field()
    key = scrapy.Field()
    catalogue_code = scrapy.Field()
    details_url = scrapy.Field()
