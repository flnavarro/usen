# -*- coding: utf-8 -*-
from scrapy.crawler import CrawlerProcess
import settings
from spiders.cctv_spider import CctvSpider
import argparse
import xlwt
import xlrd


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

    def download_tracks(self):
        # TODO: GO BY SHOW
        path = '/Users/felipelnv/Desktop/CCTV_Results/01 全球中文音乐榜上榜/'
        to_dl_path = path + 'tracks_to_download.xls'
        to_dl_list = []
        xls = xlrd.open_workbook(to_dl_path, formatting_info=True)
        n_rows = xls.sheet_by_index(0).nrows
        sheet_read = xls.sheet_by_index(0)
        for row in range(1, n_rows):
            title = sheet_read.cell(row, 0).value
            artist = sheet_read.cell(row, 1).value
            url = sheet_read.cell(row, 2).value
            dl_idx = sheet_read.cell(row, 3).value
            to_dl_list.append({
                'title': title,
                'artist': artist,
                'url': url,
                'index': dl_idx
            })
        to_dl_list = sorted(to_dl_list, key=lambda to_dl_list: to_dl_list['index'])
        last_tracks = []
        checkfile_path = path + 'last_tracks.xls'
        xls = xlrd.open_workbook(checkfile_path, formatting_info=True)
        n_rows = xls.sheet_by_index(0).nrows
        sheet_read = xls.sheet_by_index(0)
        for row in range(1, n_rows):
            title = sheet_read.cell(row, 0).value
            artist = sheet_read.cell(row, 1).value
            url = sheet_read.cell(row, 2).value
            last_tracks.append({
                'title': title,
                'artist': artist,
                'url': url,
            })
        tracks_to_dl = []
        for track in to_dl_list:
            if track['title'] == last_tracks[0]['title'] \
                    and track['artist'] == last_tracks[0]['artist'] \
                    and track['url'] == last_tracks[0]['url']:
                idx = to_dl_list.index(track)
                all_same = True
                i_max = 5
                if len(last_tracks) < 5:
                    i_max = len(last_tracks)
                for i in range(1, i_max):
                    if to_dl_list[idx + i]['title'] == last_tracks[i]['title'] \
                            and to_dl_list[idx + i]['artist'] == last_tracks[i]['artist'] \
                            and to_dl_list[idx + i]['url'] == last_tracks[i]['url']:
                        pass
                    else:
                        all_same = False
                        break
                if all_same:
                    break
            else:
                tracks_to_dl.append(track)
        # TODO: HERE DOWNLOAD
        print('SOMETHING')


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
    cctv_crawler.download_tracks()
    # yt_downloader = YoutubeDownloader()
    # track_info = artist + ' - ' + title
    # yt_downloader.download(url, self.path, track_info)
