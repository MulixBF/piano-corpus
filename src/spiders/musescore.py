# -*- coding: utf-8 -*-
import scrapy


class MusescoreSpider(scrapy.Spider):
    name = "musescore"
    allowed_domains = ["https://musescore.com"]

    sets = (
        'https://musescore.com/opengoldberg/sets/openwtc',
        'https://musescore.com/opengoldberg/sets/open-goldberg-variations-public-review'
    )

    individual_scores = (
        'https://musescore.com/user/982166/scores/979316',
        'https://musescore.com/user/10140086/scores/2448256',
        'https://musescore.com/user/36186/scores/57760'
    )

    def start_requests(self):
        login_url = 'www.https://musescore.com/user/login'
        scrapy.Request(login_url, self.login)

    def login(self, response):
        scrapy.FormRequest.from_response(response,
                                         formid='user-login',
                                         formdata={'name': 'andymulx@gmail.com', 'pass': 'chym&yaWf0'},
                                         callback=self.scrape)

    def scrape(self, response):
        for url in self.sets:


    def scrape_set(self, response):
        pass

    def scrape_score(self, response):
        pass