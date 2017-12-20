# -*- coding: utf-8 -*-
import os
import calendar
import scrapy
import xlwt
import xlrd
from scrapy.http import HtmlResponse
import pytz
import datetime


class UsenSpider(scrapy.Spider):
    name = "Usen"

    def __init__(self):
        self.root_url = 'http://music.usen.com/nowplay/sound-planet/'

        self.forms = []
        self.build_forms()

    def build_forms(self):
        print('Building forms...')
        time_japan = datetime.datetime.now(tz=pytz.timezone('Asia/Tokyo'))
        day = str(time_japan.day).zfill(2)
        month = str(time_japan.month).zfill(2)
        year = str(time_japan.year)
        hour = str(time_japan.hour)
        min = str(time_japan.min)
        band = 'A'
        chno = '06'
        npsearch = '検索'
        form = {
            'npdate': year + month + day,
            'nphour': hour,
            'npmin': min,
            'band': band,
            'chno': chno,
            'npsearch': npsearch
        }
        self.forms.append(form)

    def get_previous_day(self):
        pass

    def start_requests(self):
        yield scrapy.Request(url=self.root_url, callback=self.form_requests, errback=self.parse_error)

    def form_requests(self, response):
        # TODO: Request is not totally right. Something to do with javascript?
        for form in self.forms:
            yield scrapy.FormRequest.from_response(
                response,
                formxpath="//form[@action='http://music.usen.com/nowplay/sound-planet/']",
                formdata=form,
                callback=self.parse)

    def parse(self, response):
        # print('Getting tracks for form request... ' + response.request.body)
        #
        # titles = response.css('span.track::text').extract()
        # artists = response.css('span.artist::text').extract()
        #
        # for title in titles:
        #     artist = artists[titles.index(title)].title()
        #     title = title.title()
        #     print('Appending Track -> ' + '"' + title + '"' + ' by ' + artist)
        #
        #     already_in_tracks = False
        #     index_in_tracks = 0
        #     for track in self.all_tracks:
        #         if title == track[0] and artist == track[1]:
        #             already_in_tracks = True
        #             index_in_tracks = self.all_tracks.index(track)
        #             break
        #     if already_in_tracks:
        #         self.all_tracks[index_in_tracks][2] += 1
        #     else:
        #         self.all_tracks.append([title, artist, 1])
        # print('...tracks of form request [ ' + response.request.body + ' ] finished.')
        # self.save_list()
        pass

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
