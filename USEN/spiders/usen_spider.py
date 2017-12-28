# -*- coding: utf-8 -*-
import os
import scrapy
import xlwt
import xlrd
import datetime
import json
from metadata_formatter import format_metadata
import time


class UsenSpider(scrapy.Spider):
    name = "Usen"

    def __init__(self, path):
        self.bands = [
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K'
        ]

        self.channels = [
            range(6, 58), range(1, 73), range(1, 71),
            range(1, 66), range(16, 20), [9, 22],
            [36, 40], [1, 2] + range(7, 41), range(1, 62),
            range(1, 62), range(1, 5) + range(6, 30) + range(31, 37) + [38] + range(40, 64)
        ]

        self.utc_date = ''
        self.utc_hour = ''
        self.utc_min = ''

        self.path = path

    def get_current_utc_time(self):
        utc_now = datetime.datetime.utcnow()
        self.utc_date = str(utc_now.year) + str(utc_now.month).zfill(2) + str(utc_now.day).zfill(2)
        self.utc_hour = str(utc_now.hour).zfill(2)
        self.utc_min = str(utc_now.minute).zfill(2)

    def start_requests(self):
        while True:
            for band in self.bands:
                idx = self.bands.index(band)
                for channel in self.channels[idx]:
                    chno = str(channel).zfill(2)
                    url = 'http://music.usen.com/usencms/search_nowplay1.php?npband=' + band \
                          + '&npch=' + chno + '&nppage=yes'
                    self.get_current_utc_time()
                    yield scrapy.Request(
                        url=url,
                        meta={'band': band,
                              'chno': chno,
                              'utc_date': self.utc_date,
                              'utc_hour': self.utc_hour,
                              'utc_min': self.utc_min},
                        callback=self.parse,
                        errback=self.parse_error,
                        dont_filter=True
                    )
            time.sleep(30)

    def parse(self, response):
        band = response.request.meta['band']
        chno = response.request.meta['chno']
        date = response.request.meta['utc_date']
        hour = response.request.meta['utc_hour']
        min = response.request.meta['utc_min']
        print('BAND: ' + band + ' // CHNO: ' + chno)

        track = response.xpath(".//ul[@class='clearfix np-now']//li[@class='np03']/text()").extract_first()

        tracks_today = self.read_list(band, chno, date)

        if track is not None:
            title, artist = format_metadata(track)
            track_is_new = True
            if len(tracks_today) > 0:
                if title == tracks_today[-1]['title'] and artist == tracks_today[-1]['artist']:
                    print('Current track already in list.')
                    track_is_new = False
            if track_is_new:
                tracks_today.append({
                    'title': title,
                    'artist': artist,
                    'utc_time': hour + ':' + min
                })
                print('Adding track: "' + title + '"' + ' by ' + artist + ' // Time: ' + hour + ':' + min)
                self.save_list(tracks_today, band, chno, date)
        else:
            print('No tracks available.')

    def read_list(self, band, chno, date):
        tracks_today = []
        if os.path.exists(self.path):
            folder_path = self.path + '/' + band + chno
            if os.path.exists(folder_path):
                file_path = folder_path + '/' + band + chno + '_' + date + '.xls'
                if os.path.exists(file_path):
                    xls = xlrd.open_workbook(file_path, formatting_info=True)
                    n_rows = xls.sheet_by_index(0).nrows
                    sheet_read = xls.sheet_by_index(0)
                    for row in range(1, n_rows):
                        title = sheet_read.cell(row, 0).value
                        artist = sheet_read.cell(row, 1).value
                        utc_time = sheet_read.cell(row, 2).value
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

    def save_list(self, tracks_today, band, chno, date):
        list_xls = xlwt.Workbook()
        sheet = list_xls.add_sheet(band + chno + '_' + date)
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
        file_path = folder_path + '/' + band + chno + '_' + date + '.xls'
        list_xls.save(file_path)

    def parse_error(self, response):
        print('There was a response error of type -> ' + response.value.response.status)
