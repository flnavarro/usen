# -*- coding: utf-8 -*-
import os
import calendar
import scrapy
import xlwt
import xlrd
from scrapy.http import HtmlResponse
import pytz
import datetime
import scrapy_splash
from scrapy_splash import SplashRequest
from scrapy_splash import SplashFormRequest
import urlparse
import json


class UsenSpider(scrapy.Spider):
    name = "Usen"

    def __init__(self):
        self.root_url = 'http://music.usen.com/nowplay/sound-planet/'

        self.bands = [
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K'
        ]
        self.bands = ['E', 'F', 'G']
        self.channels = []
        # self.channels.append(range(6, 58))
        # self.channels.append(range(1, 73))
        # self.channels.append(range(1, 71))
        # self.channels.append(range(1, 66))
        self.channels.append(range(16, 20))
        self.channels.append([9, 22])
        self.channels.append([36, 40])
        # self.channels.append(range(1, 41))
        # self.channels.append(range(1, 62))
        # self.channels.append(range(1, 62))
        # self.channels.append(range(1, 64))

        self.forms = []
        self.tracks_now = []
        self.build_forms()

    def build_forms(self):
        print('Building forms...')
        time_japan = datetime.datetime.now(tz=pytz.timezone('Asia/Tokyo'))
        date = str(time_japan.year) + str(time_japan.month).zfill(2) + str(time_japan.day).zfill(2)
        hour = str(time_japan.hour)
        min = str(time_japan.minute)
        for band in self.bands:
            idx = self.bands.index(band)
            for channel in self.channels[idx]:
                chno = str(channel).zfill(2)
                npsearch = '検索'
                form = {
                    'npdate': date,
                    'nphour': hour,
                    'npmin': min,
                    'band': band,
                    'chno': chno,
                    'npsearch': npsearch
                }
                self.forms.append(form)
                self.tracks_now.append(
                    {
                        'band': band,
                        'chno': str(channel).zfill(2),
                        'available': True,
                        'tracks': list()
                    }
                )

    def start_requests(self):
        yield SplashRequest(
            self.root_url,
            self.form_requests,
            endpoint='render.json',
            args={
                'wait': 5.0,
                'har': 1,
                'html': 1,
            }
        )

    def form_requests(self, response):
        for form in self.forms:
            yield SplashFormRequest.from_response(
                response,
                formxpath="//form[@action='http://music.usen.com/nowplay/sound-planet/']",
                formdata=form,
                endpoint='render.json',
                args={
                    'wait': 5.0,
                    'har': 1,
                    'html': 1,
                },
                clickdata={
                    "name": "npsearch",
                    "type": "submit"
                },
                callback=self.parse
            )

    def parse(self, response):
        request_body = json.loads(response.request.body.decode('utf-8'))['body']
        query = dict(urlparse.parse_qsl(urlparse.urlsplit(self.root_url[:-1] + '.html?' + request_body).query))
        band = query['band']
        chno = query['chno']
        track = response.xpath(".//ul[@class='clearfix np-now']//li[@class='np03']/text()").extract_first()
        # TODO: Here we check if we have more tracks
        # TODO: missing than just the NOW one
        # TODO: and append them in order
        if track != '' and track != list():
            for track_now in self.tracks_now:
                if track_now['band'] == band and track_now['chno'] == chno:
                    # TODO: Use metadata formatter here
                    # TODO: Save all new tracks in csv here
                    track_now['tracks'].append(track)
                    print('Bd:' + band + ' // Ch:' + chno + ' // Track:' + track)

    def parse_error(self, response):
        # if response.value.response.status == 408 or response.value.response.status == 500 \
        #         or response.value.response.status == 503:
        #     # Error 408 -> Request Timeout
        #     # Error 500 -> Internal Server Error
        #     # Error 503 -> Service Unavailable
        #     self.repair_sheet.write(self.repair_row, 0, response.request.body)
        #     self.repair_xls.save(self.folder_path + self.radio_station + '_repair.xls')
        #     self.repair_row += 1
        #     print('There was an error of type -> ' + str(response.value.response.status))
        #     print('Saved form to repair -> ' + str(response.request.body))
        # else:
        #     # Other
        #     # Error 400 -> Bad Request
        #     # Error 404 -> Not Found
        #     print('There was an error of type -> ' + str(response.value.response.status))
        pass

    def save_list(self):
        # self.list_xls = xlwt.Workbook()
        # self.sheet = self.list_xls.add_sheet(self.radio_station + 'Playlist')
        # self.sheet.write(0, 0, 'Track Title')
        # self.sheet.write(0, 1, 'Track Artist')
        # self.sheet.write(0, 2, 'Count')
        # # self.sheet.write(0, 3, 'URL From')
        # self.row = 1
        # list_index = 1
        # for track in self.all_tracks:
        #     self.sheet.write(self.row, 0, track[0])
        #     self.sheet.write(self.row, 1, track[1])
        #     self.sheet.write(self.row, 2, track[2])
        #     # self.sheet.write(self.row, 3, response.url)
        #     self.row += 1
        #     if self.row == 30001:
        #         list_index += 1
        #         self.sheet = self.list_xls.add_sheet(self.radio_station + 'Playlist (' + str(list_index) + ')')
        #         self.sheet.write(0, 0, 'Track Title')
        #         self.sheet.write(0, 1, 'Track Artist')
        #         self.sheet.write(0, 2, 'Play Count')
        #         self.row = 1
        # if not self.repair_opt:
        #     self.list_xls.save(self.folder_path + self.radio_station + '_' + self.saving_code + '.xls')
        # else:
        #     self.list_xls.save(self.folder_path + self.radio_station + '_' + self.saving_code + '_repaired.xls')
        pass
