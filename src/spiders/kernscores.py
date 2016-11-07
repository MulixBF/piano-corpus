# -*- coding: utf-8 -*-
import scrapy

from src.items import Composition


class KernscoresSpider(scrapy.Spider):
    name = 'kernscores'
    allowed_domains = ['kern.ccarh.org', 'kern.humdrum.org']
    start_urls = (
        'http://kern.humdrum.org/cgi-bin/browse?l=musedata/bach/keyboard/wtc',
        'http://kern.ccarh.org/cgi-bin/ksbrowse?type=collection&l=/users/craig/classical/beethoven/piano/sonata',
        'http://kern.ccarh.org/cgi-bin/ksbrowse?type=collection&l=/users/craig/classical/scarlatti/longo',
        'http://kern.ccarh.org/cgi-bin/ksbrowse?type=collection&l=/users/craig/classical/mozart/piano/sonata',
        'http://kern.ccarh.org/cgi-bin/ksbrowse?type=collection&l=/users/craig/classical/haydn/keyboard/uesonatas',
        'http://kern.ccarh.org/cgi-bin/ksbrowse?type=collection&l=/users/craig/classical/clementi/op36',
        'http://kern.ccarh.org/cgi-bin/ksbrowse?type=collection&l=/users/craig/classical/brahms/op01',
        'http://kern.ccarh.org/cgi-bin/ksbrowse?type=collection&l=/users/craig/classical/grieg/op07',
        'http://kern.humdrum.org/cgi-bin/kern/kssearch?s=t&keyword=mazurka',
        'http://kern.ccarh.org/cgi-bin/ksbrowse?type=collection&l=/users/craig/classical/chopin/prelude',
        'http://kern.humdrum.org/browse?l=joplin',
        'http://kern.humdrum.org/search?s=t&keyword=Pachelbel',
        'http://kern.humdrum.org/search?s=t&keyword=Scriabin',
        'http://kern.humdrum.org/cgi-bin/browse?l=osu/classical/chopin',
    )

    # noinspection PyMethodMayBeStatic
    def _get_row_data(self, response, row_title):
        row = response.xpath('//tr[td/i[text()="{0}"]]'.format(row_title))

        if not row:
            return ''

        data = row.xpath('td[last()]/text()').extract_first()
        return data

    # noinspection PyMethodMayBeStatic
    def _get_midi_url(self, response):
        link = response.xpath('//a[contains(text(), ".mid")]')
        return link.xpath("@href").extract_first()

    def _parse_info_page(self, response):
        self.logger.info('Parsing info page: ' + response.url)

        item = Composition()
        item['composer'] = self._get_row_data(response, 'Composer')
        item['name'] = self._get_row_data(response, 'Title')
        item['key'] = self._get_row_data(response, 'Primary Music Key')
        item['catalogue_code'] = self._get_row_data(response, 'Scholarly cat. num.')
        item['genre'] = self._get_row_data(response, 'Style, period, or type of work designation')
        item['year'] = self._get_row_data(response, 'Date of composition')
        item['details_url'] = response.url
        item['file_urls'] = [self._get_midi_url(response)]

        yield item

    def parse(self, response):
        info_links = response.xpath('//a[contains(@href, "format=info")]')

        for link in info_links:
            url = link.xpath('@href').extract_first()
            yield scrapy.Request(url, self._parse_info_page)
