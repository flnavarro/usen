# -*- coding: utf-8 -*-
from scrapy.crawler import CrawlerProcess
import settings
from spiders.cctv_spider import CctvSpider
import argparse
from batch_manager import BatchManager


class CctvCrawler(object):

    def __init__(self, batches_path, n_tracks_per_batch, first_execution):
        self.spider = CctvSpider
        self.process = None
        self.batches_path = batches_path
        self.n_tracks_per_batch = n_tracks_per_batch
        self.first_execution = first_execution

    def crawl_tracks(self):
        self.process = CrawlerProcess({
            'USER AGENT': settings.USER_AGENT
        })
        self.process.crawl(self.spider, path=self.batches_path, first_execution=self.first_execution)
        self.process.start()

    def make_batches(self):
        batch_manager = BatchManager(self.n_tracks_per_batch, self.batches_path, self.first_execution)
        batch_manager.make_batches()


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
    cctv_crawler.crawl_tracks()
else:
    # cctv_path = '/Users/felipelnv/Desktop/CCTV_Results/'
    cctv_path = '/Volumes/HD2/CCTV_Results/'
    cctv_crawler = CctvCrawler(cctv_path, n_tracks_per_batch=100, first_execution=False)
    # cctv_crawler.crawl_tracks()
    cctv_crawler.make_batches()

