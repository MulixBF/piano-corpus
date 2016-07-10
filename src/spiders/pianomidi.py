# -*- coding: utf-8 -*-
import scrapy
import re
from urllib.parse import urljoin
from collections import namedtuple

from src.items import Composition

Part = namedtuple('Part', ['name', 'midi_url'])
BASE_URL = 'http://www.piano-midi.de/'


def _parse_title_string(title_string):
    match = re.match('(.*)\((\d{4})\)', title_string)
    if not match:
        return title_string, None

    title = match.group(1).strip()
    year = match.group(2).strip()

    return title, year


class PianomidiSpider(scrapy.Spider):
    name = "pianomidi"

    allowed_domains = ["www.piano-midi.de"]
    start_urls = (
        'http://www.piano-midi.de/midi_files.htm',
    )

    def parse(self, response):
        composer_rows = response.css('tr.midi')[1:]

        for row in composer_rows:
            cells = row.css('td')
            link = cells[0].css('::attr(href)').extract_first()
            composer = cells[0].css('::text').extract_first()
            genre = cells[3].css('::text').extract_first()
            url = urljoin(BASE_URL, link)

            yield scrapy.Request(url, self.parse_composer_page, meta={
                'composer': composer,
                'genre': genre
            })

    def parse_composer_page(self, response):
        title_strings = response.css('h2::text').extract()
        part_tables = response.css('h2+table')

        assert len(title_strings) == len(part_tables)

        self.logger.info(
            'Parsing composer {0}. Compositions: {1}'.format(response.meta['composer'], len(title_strings)))

        for title_string, parts_table in zip(title_strings, part_tables):
            part_rows = parts_table.css('tr.midi')[1:]
            parts = list(map(self.parse_part_row, part_rows))
            self.logger.info('Parsing {0} found {1} pieces'.format(title_string, len(parts)))
            for item in self.parse_multipart_composition(response, title_string, parts):
                yield item

    # noinspection PyMethodMayBeStatic
    def parse_multipart_composition(self, response, title_string, parts):
        composition_name, year = _parse_title_string(title_string)

        for part in parts:
            self.logger.info('midi url: ' + part.midi_url)
            item = Composition()
            item['name'] = '{0} {1}'.format(composition_name, part.name)
            item['genre'] = response.meta['genre']
            item['composer'] = response.meta['composer']
            item['instruments'] = ['Piano']
            item['year'] = year
            item['details_url'] = response.url
            item['file_urls'] = [part.midi_url]

            yield item

    # noinspection PyMethodMayBeStatic
    def parse_part_row(self, row):
        link = row.css('td:first-child>a')
        title = link.css('::text').extract_first()
        midi_url_rel = link.css('::attr(href)').extract_first()
        midi_url = urljoin(BASE_URL, midi_url_rel)
        return Part(title, midi_url)
