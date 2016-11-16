import scrapy as sp
import logging
import time
from urllib.parse import urljoin
from src import utils
from src.items import MusescoreComposition

logging.basicConfig(level=logging.INFO, filename=time.strftime('logs/%Y%m%d-%H%M%S-musescore.log'))


class MusescoreSpider(sp.Spider):

    def __init__(self, input_file='scores.txt'):

        super().__init__()

        self.sets = []
        self.scores = []

        with open(input_file, 'r') as f:
            for line in f.readlines():

                kind, url = line.split(':')

                if kind == 'set':
                    self.sets.append(url.strip())
                elif kind == 'score':
                    self.scores.append(url.strip())
                else:
                    raise ValueError('Line should have format (set|score): <url>')

    name = 'musescore'
    base_url = 'https://musescore.com/'
    allowed_domains = ['musescore.com']

    login_path = 'user/login'
    username = 'sidedeb'
    password = 'sidedeb'

    custom_settings = {
        'DOWNLOAD_DELAY': 1
    }

    def start_requests(self):
        login_url = urljoin(self.base_url, 'user/login')
        logging.debug('Starting spider...')
        logging.debug('Sets to crawl:\n%s', '\n'.join(self.sets))
        logging.debug('Scores to crawl:\n%s', '\n'.join(self.scores))

        yield sp.Request(login_url, self.login)

    def login(self, response):
        logging.info('Login page loaded. Trying to log in...')
        yield sp.FormRequest.from_response(response,
                                           formid='user-login',
                                           formdata={'name': self.username, 'pass': self.password},
                                           callback=self.parse)

    def parse(self, response):

        if response.css('body.not-logged-in'):
            raise Exception('Login failed')

        logging.info('Login succeeded. Crawling...')

        for set_url in self.sets:
            yield sp.Request(urljoin(self.base_url, set_url), self.scrape_set)

        for score_url in self.scores:
            yield sp.Request(urljoin(self.base_url, score_url), self.scrape_score)

    def scrape_set(self, response):

        score_links = response.css('div.view-content span.field-content>a')
        next_link = response.css('ul.pager li.pager-next>a')
        page_title = response.css('h1.title')

        set_name = page_title.css('::text').extract()

        logging.info('Parsing set "%s". Found %d scores...', set_name, len(score_links))
        score_urls = [utils.get_link_url(link, self.base_url) for link in score_links]

        for url in score_urls:
            yield sp.Request(url, self.scrape_score)

        if next_link:
            assert len(next_link) == 1
            next_page_url = utils.get_link_url(next_link[0], self.base_url)

            logging.info('Found next page link for set %s', set_name)
            yield sp.Request(next_page_url, self.scrape_set)

    def scrape_score(self, response):
        score_info = self._parse_info_grid(response)

        item = MusescoreComposition()
        item['name'] = response.css('h1.title::text')[0].extract()
        item['instruments'] = score_info['Parts']
        item['tags'] = response.css('div.score-tags a::text').extract()
        item['key'] = score_info['Key signature']
        item['duration'] = score_info['Duration']
        item['file_urls'] = [url for url in self.get_download_url(response) if url.endswith('mid')]

        item['username'] = response.css('span.username a::text')[0].extract()
        item['paid_user'] = bool(response.css('span.username a.pro-badge'))
        item['license'] = score_info['License']

        score_stats = response.css('ul.score-stats li var::text')
        item['view_count'] = score_stats[0].extract() if score_stats else 0
        item['star_count'] = score_stats[1].extract() if score_stats else 0

        logging.info('Scraped item %s...', item['name'])
        yield item

    def get_download_url(self, response):
        download_links = response.css('#score-download-list a')
        return [utils.get_link_url(link, self.base_url) for link in download_links]

    def _parse_info_grid(self, response):
        score_info = {}
        info_grid = response.css('table.info-grid')

        for row in info_grid.css('tr'):
            key = row.css('th::text')[0].extract()
            value = self._parse_info_grid_value(row.css('td'))
            score_info[key] = value

        return score_info

    @staticmethod
    def _parse_info_grid_value(value_cell):

        if value_cell.css('ul'):
            return [x.extract() for x in value_cell.css('ul li::text')]

        return value_cell.css('::text')[0].extract()
