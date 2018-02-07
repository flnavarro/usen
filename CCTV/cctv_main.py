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
        self.parser = argparse.ArgumentParser(description="Download CCTV's Tracks")
        self.batches_path = ''
        self.n_tracks_per_batch = 100
        self.first_execution = False

    def add_arguments(self):
        self.parser.add_argument('-path', action='store', dest='path', required=True,
                                 help='Path where batches will be stored.')
        self.parser.add_argument('-n_tracks', metavar='n_tracks', type=int, required=True,
                                 help='Number of tracks per batch.')
        self.parser.add_argument('-first_execution', action='store_true', dest='first_execution', default=False,
                                 help='Choose this option for the first execution of this script.')

    def parse_input(self):
        self.add_arguments()
        args = self.parser.parse_args()
        self.batches_path = args.path
        self.n_tracks_per_batch = args.n_tracks
        self.first_execution = args.first_execution


args_input = False

if args_input:
    input_parser = InputParser()
    input_parser.parse_input()
    batches_path = input_parser.batches_path
    n_tracks_per_batch = input_parser.n_tracks_per_batch
    first_execution = input_parser.first_execution
    cctv_crawler = CctvCrawler(batches_path, n_tracks_per_batch, first_execution)
    cctv_crawler.crawl_tracks()
    cctv_crawler.make_batches()
else:
    batches_path = '/Volumes/HD2/CCTV_Results/'
    cctv_crawler = CctvCrawler(batches_path, n_tracks_per_batch=100, first_execution=True)
    # cctv_crawler.crawl_tracks()
    cctv_crawler.make_batches()

