# -*- coding: utf-8 -*-
from scrapy.crawler import CrawlerProcess
from USEN import settings
from spiders.usen_spider import UsenSpider


class UsenCrawler(object):

    def __init__(self):
        self.spider = UsenSpider
        self.process = None

    def get_current_tracks(self):
        self.process = CrawlerProcess({
            'USER AGENT': settings.USER_AGENT,
            'SPLASH_URL': settings.SPLASH_URL,
            'DOWNLOADER_MIDDLEWARES': settings.DOWNLOADER_MIDDLEWARES,
            'SPIDER_MIDDLEWARES': settings.SPIDER_MIDDLEWARES,
            'DUPEFILTER_CLASS': settings.DUPEFILTER_CLASS,
            'HTTPCACHE_STORAGE': settings.HTTPCACHE_STORAGE
        })
        self.process.crawl(self.spider, path='/Users/felipelnv/Desktop/USEN_Results')
        self.process.start()


usen_crawler = UsenCrawler()
usen_crawler.get_current_tracks()