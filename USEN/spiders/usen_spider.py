# -*- coding: utf-8 -*-
import os
import scrapy
import xlwt
import xlrd
from scrapy.http import HtmlResponse
import pytz
import datetime
from scrapy_splash import SplashRequest
from scrapy_splash import SplashFormRequest
import urlparse
import json
from metadata_formatter import format_metadata
import time


class UsenSpider(scrapy.Spider):
    name = "Usen"

    def __init__(self, path):
        self.root_url = 'http://music.usen.com/nowplay/sound-planet/'

        self.bands = [
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K'
        ]
        self.channels = []
        self.channels.append(range(6, 58))
        self.channels.append(range(1, 73))
        self.channels.append(range(1, 71))
        self.channels.append(range(1, 66))
        self.channels.append(range(16, 20))
        self.channels.append([9, 22])
        self.channels.append([36, 40])
        self.channels.append(range(1, 41))
        self.channels.append(range(1, 62))
        self.channels.append(range(1, 62))
        self.channels.append(range(1, 64))

        # # DEBUG
        # self.bands = ['F', 'G']
        # self.channels = []
        # self.channels.append([9, 22])
        # self.channels.append([36, 40])

        self.forms = []
        self.tracks_now = []

        self.utc_date = ''
        self.utc_hour = ''
        self.utc_min = ''

        self.path = path

    def get_current_utc_time(self):
        print('Get current UTC time...')
        utc_now = datetime.datetime.utcnow()
        self.utc_date = str(utc_now.year) + str(utc_now.month).zfill(2) + str(utc_now.day).zfill(2)
        self.utc_hour = str(utc_now.hour)
        self.utc_min = str(utc_now.minute)

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
                        'title': list(),
                        'artist': list()
                    }
                )

    def start_requests(self):
        yield SplashRequest(
            self.root_url,
            self.form_requests,
            endpoint='render.json',
            args={
                'wait': 1.0,
                'har': 1,
                'html': 1,
            }
        )

    def form_requests(self, response):
        while True:
            self.build_forms()
            self.get_current_utc_time()
            for form in self.forms:
                yield SplashFormRequest.from_response(
                    response,
                    formxpath="//form[@action='http://music.usen.com/nowplay/sound-planet/']",
                    formdata=form,
                    endpoint='render.json',
                    args={
                        'wait': 1.0,
                        'har': 1,
                        'html': 1,
                    },
                    clickdata={
                        "name": "npsearch",
                        "type": "submit"
                    },
                    callback=self.parse
                )
            time.sleep(30)

    def parse(self, response):
        request_body = json.loads(response.request.body.decode('utf-8'))['body']
        query = dict(urlparse.parse_qsl(urlparse.urlsplit(self.root_url[:-1] + '.html?' + request_body).query))
        band = query['band']
        chno = query['chno']
        track = response.xpath(".//ul[@class='clearfix np-now']//li[@class='np03']/text()").extract_first()
        if track is not None:
            tracks_today = self.read_list(band, chno)
            title, artist = format_metadata(track)
            if title == tracks_today[-1]['title'] and artist == tracks_today[-1]['artist']:
                pass
            else:
                tracks_today.append({
                    'title': title,
                    'artist': artist,
                    'utc_time': self.utc_hour + ':' + self.utc_min
                })
                print(
                        'Adding track: "' + title + '"' + ' by ' + artist + ' // Time: ' + self.utc_hour + ':' + self.utc_min)
                self.save_list(tracks_today, band, chno)
        else:
            print('track is none')

    def read_list(self, band, chno):
        tracks_today = []
        if os.path.exists(self.path):
            folder_path = self.path + '/' + band + chno
            if os.path.exists(folder_path):
                file_path = folder_path + '/' + band + chno + '_' + self.utc_date + '.xls'
                if os.path.exists(file_path):
                    xls = xlrd.open_workbook(file_path, formatting_info=True)
                    n_rows = xls.sheet_by_index(0).nrows
                    sheet_read = xls.sheet_by_index(0)
                    for row in range(1, n_rows):
                        title = sheet_read.cell(row, 0).value
                        artist = sheet_read.cell(row, 1).value
                        utc_time = sheet_read.cell(row, 2).value
                        print('Reading track: "' + title + '"' + ' by ' + artist + ' // Time: ' + utc_time)
                        tracks_today.append({
                            'title': title,
                            'artist': artist,
                            'utc_time': utc_time
                        })
            else:
                os.makedirs(self.path + '/' + band + chno)
        else:
            print('The path specified does not exist')
        return tracks_today

    def save_list(self, tracks_today, band, chno):
        list_xls = xlwt.Workbook()
        sheet = list_xls.add_sheet(band + chno + '_' + self.utc_date)
        sheet.write(0, 0, 'Track Title')
        sheet.write(0, 1, 'Track Artist')
        sheet.write(0, 2, 'UTC Time')
        row = 1
        for track in tracks_today:
            sheet.write(row, 0, track['title'])
            sheet.write(row, 1, track['artist'])
            sheet.write(row, 2, track['utc_time'])
            row += 1
        folder_path = self.path + '/' + band + chno
        file_path = folder_path + '/' + band + chno + '_' + self.utc_date + '.xls'
        list_xls.save(file_path)

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
        print('THERE WAS A RESPONSE ERROR! -> ' + response.value.response.status)
