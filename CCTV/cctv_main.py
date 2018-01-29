# -*- coding: utf-8 -*-
from scrapy.crawler import CrawlerProcess
import settings
from spiders.cctv_spider import CctvSpider
import argparse


class CctvCrawler(object):

    def __init__(self, path):
        self.spider = CctvSpider
        self.process = None
        self.path = path

    def get_current_tracks(self):
        self.process = CrawlerProcess({
            'USER AGENT': settings.USER_AGENT
        })
        self.process.crawl(self.spider, path=self.path)
        self.process.start()


class InputParser(object):
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Get Usen's Playlists Data")
        self.path = ''

    def add_arguments(self):
        self.parser.add_argument('-path', action='store', dest='path', required=True,
                                 help='Path where lists will be stored.')

    def parse_input(self):
        self.add_arguments()
        args = self.parser.parse_args()
        self.path = args.path


args_input = False

if args_input:
    input_parser = InputParser()
    input_parser.parse_input()
    cctv_path = input_parser.path
    cctv_crawler = CctvCrawler(cctv_path)
    cctv_crawler.get_current_tracks()
else:
    cctv_path = '/Users/felipelnv/Desktop/CCTV_Results/'
    cctv_crawler = CctvCrawler(cctv_path)
    cctv_crawler.get_current_tracks()
