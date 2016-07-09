# -*- coding: utf-8 -*-
import scrapy
import re
from urllib import parse
from src.items import Composition

BASE_URL = 'http://www.mutopiaproject.org'


def _extract_cell_text(table, row, col, postpocess=None):
    selector = 'tr:nth-child({row}) td:nth-child({col})::text'.format(row=row, col=col)
    result = table.css(selector).extract_first()

    if postpocess:
        result = postpocess(result)

    return result


def _extract_cell_link_href(table, row, col):
    selector = 'tr:nth-child(5) td:nth-child(1) a::attr(href)'.format(row=row, col=col)
    return table.css(selector).extract_first()


def _parse_composer(text):
    match = re.match('^by (.*) \(.*', text)
    if match:
        return match.group(1).strip()

    return text.strip()


def _parse_instruments(text):
    match = re.match('^for (.*)', text)

    if match:
        instruments = match.group(1).split(',')
        return list([instrument.strip() for instrument in instruments])

    return [text]


def _extract_next_page_url(link):
    relative_url = link.css('::attr(href)').extract_first()
    return parse.urljoin(BASE_URL + '/cgibin/', relative_url)


class MutopiaProjectSpider(scrapy.Spider):

    name = 'mutopiaproject'
    allowed_domains = ['www.mutopiaproject.org']
    start_urls = (BASE_URL + '/cgibin/make-table.cgi?Instrument=Piano',)

    def parse(self, response):
        tables = response.css('table.result-table')

        if not tables:
            return

        for table in tables:
            item = Composition()
            item['name'] = _extract_cell_text(table, 1, 1)
            item['composer'] = _extract_cell_text(table, 1, 2, _parse_composer)
            item['catalogue_code'] = _extract_cell_text(table, 1, 3)
            item['instruments'] = _extract_cell_text(table, 2, 1, _parse_instruments)
            item['year'] = _extract_cell_text(table, 2, 2)
            item['genre'] = _extract_cell_text(table, 2, 3)
            item['details_url'] = _extract_cell_link_href(table, 3, 3)
            item['file_urls'] = [_extract_cell_link_href(table, 4, 2)]

            yield item

        next_page_link = response.css('a:contains("Next 10")')
        next_page_url = _extract_next_page_url(next_page_link)
        self.logger.info('following link: ' + next_page_url)
        yield scrapy.Request(next_page_url, self.parse)
