# -*- coding: utf-8 -*-
import os
import scrapy
import xlwt
import xlrd
import datetime
import json
import base64
import ast
from math import ceil
from metadata_formatter import format_metadata
import time
import scrapy_splash
from scrapy_splash import SplashRequest
from scrapy_splash import SplashFormRequest


class CctvSpider(scrapy.Spider):
    name = "Cctv"

    def __init__(self, path):
        self.shows = [
            # SHOW TITLE, URL, SINGLE SONGS SECTION
            # es el parametro p= el que dice el número de página
            # se cargan los resultados de la pagina (18) en json
            # también muestra el numero total de tracks disponibles
            ['全球中文音乐榜上榜', 'TOPC1451542061864640', 'Y2oSEQdYWBBlMZCIG7UF160128', '精彩看点', 0],
        ]

        self.formats = [
            {'url': 'http://api.cntv.cn/lanmu/videolistByColumnId?',
             'service_url': '&serviceId=tvcctv&type=1&n=',
             'items': 100,
             'json_cb': '&t=jsonp&cb=setItemByidELMT'},
        ]

        self.all_shows = [
            ['全球中文音乐榜上榜', 'TOPC1451542061864640', 'Y2oSEQdYWBBlMZCIG7UF160128', '精彩看点'],
            ['一起音乐吧', 'TOPC1451542132455743', 'Wko1T9K7rSHVc6q1rLNO160128', '精彩看点'],
            ['CCTV音乐厅', 'TOPC1451534421925242', 'JvrTH46rtYodBaNy2EAY160128', '精彩看点'],
            ['民歌·中国', 'TOPC1451541994820527', '6wZ1ivCiqkK3IdsDR7Ue160128', '精彩看点'],
            ['音乐传奇', 'TOPC1451542222069826', 'o14lfceelMrQgl1f4HJP160128', '精彩看点'],

            ['风华国乐', 'TOPC1451534503915324', 'Rd5X7WcB5FbgFfzQD4y1160128', '精彩看点'],
            ['精彩音乐汇', 'TOPC1451541414450906', 'ci3czCDkMCHn1Sm3GUYP160128', '精彩看点'],
            ['影视留声机', 'TOPC1451542346007956', 'aMYYOayXZUgOqOditFHk160128', '精彩看点'],
            ['中国音乐电视', 'TOPC1451542397206110', 'IJaYKRIupN0pxTX4cVlV160128', '精彩看点'],
            ['百年歌声', 'TOPC1451534465694290', 'IiqMS9z6W9gVhSwCAixq160127', '精彩看点'],

            ['乐游天下', 'TOPC1451541538046196', 'e9hO43WpPk4DP4GH0LkF160128', '精彩看点'],
            ['我要上春晚', '?', '', 'WHOLE PAGE'],
            ['星光大道', 'TOPC1451467630488780', 'KglXGa1D1WCZwhh4uaZ3160128', '精彩片段'],
            ['越战越勇', 'TOPC1451467829851129', 'A5DY1h2trsLm0RMGVjVY160206', '精彩片段'],
            ['回声嘹亮', 'TOPC1451535575561597', '', '精彩看点'],
                # # DIFFERENT!
                # 'http://api.cntv.cn/lanmu/videolistByColumnId?'
                # 'id=TOPC1451535575561597'
                # '&n=20&of=fdate&'
                # 'p=1'
                # '&type=1&serviceId=tvcctv' # type 1 is singles
                # # nothing if its this year
                # '&Y=2017&M=11' # year and month

            ['幸福账单', 'TOPC1451535575561597', 'd6wx82jRexn0Qx8hoLFU160126', '精彩看点'],
            ['黄金100秒', '?', '', 'WHOLE PAGE'],
            ['非常6+1', 'TOPC1451467940101208', '', '精彩看点'],
                # DIFFERENT! Same as previous different
            ['综艺盛典', '?', '', 'WHOLE PAGE'],
            ['天天把歌唱', '?', '', 'ENTIRE SHOWS'],

            ['星光大道超级版', '?', '', 'WHOLE PAGE'], # may work with no javascript / single page
            ['有朋远方来', '?', '', 'WHOLE PAGE'],
            ['中国正在听', '?', '', 'WHOLE PAGE'],
            ['完美星开幕', '?', '', 'WHOLE PAGE'],
            ['巅峰音乐汇', '?', '', 'WHOLE PAGE'],

            ['“中国梦”主题歌曲展播', '?', '', 'WHOLE PAGE'], # CNTV -  may work with no javascript
            ['中国民歌大会第二季', '?', '', 'WHOLE PAGE'],
            ['我和我的祖国2017', '?', '', 'WHOLE PAGE'],
            ['2017年中秋晚会', '?', '', 'WHOLE PAGE'],
            ['中秋特别节目', '?', '', 'WHOLE PAGE'],

            # FROM 31 HERE...
            ['江山如画-2017国庆音乐会', '?', '', '精彩视频'], # may work with no javascript / single page
            ['中国梦 祖国颂2017', '?', '', '精彩视频'], # DIFFERENT V2
            ['强军战旗红——建军90周年“心连心”赴南昌慰问演出', '?', '', '精彩视频'], # DIFFERENT V2
            ['在党的旗帜下', '?', '', '精彩视频'], # DIFFERENT V2
            ['守望相助草原情', '?', '', '精彩视频'], # DIFFERENT V2

            ['歌声飘过90年', '?', '', 'WHOLE'], # WHOLE PAGE
            ['唱支山歌给党听', '?', '', 'WHOLE'],
            ['山水寄美端午情', '?', '', 'WHOLE'],
            ['中国梦·劳动美2017', '?', '', 'WHOLE'],
            ['2017春晚', '?', '', 'WHOLE'],

            ['美丽中国唱起来', '?', '', 'WHOLE'], # DIFFERENT V2
            ['启航2017', '?', '', 'WHOLE'],
            ['我和我的祖国2016', '?', '', 'WHOLE'],
            ['中国梦 祖国颂2016', '?', '', 'WHOLE'],
            ['中国民歌大会第一季', '?', '', 'WHOLE'],

            ['寻找刘三姐第三季', '?', '', 'WHOLE'],
            ['心连心艺术团慰问演出', '?', '', 'WHOLE'],
            ['伟大的旗帜', '?', '', 'WHOLE'],
            ['中国梦·劳动美2016', '?', '', 'WHOLE'],
            ['2016春晚', '?', '', 'WHOLE'],

            ['启航2016', '?', '', 'WHOLE'],
            ['2015春晚', '?', '', 'WHOLE'],
            ['胜利与和平', '?', '', 'WHOLE'],
            ['中国好歌曲第三季', '?', '', 'WHOLE'],
            ['中国好歌曲第二季', '?', '', 'WHOLE'],
            ['中国好歌曲', '?', '', 'WHOLE'],
        ]

        '''
        self.root_url = 'http://api.cntv.cn/lanmu/videolistByColumnId?'
        self.service_type = '&serviceId=tvcctv&type=1&n=18&'
        self.json = '&t=jsonp&'
        id = 'TOPC1451542061864640'
        page = '1'
        id_ELMT = 'Y2oSEQdYWBBlMZCIG7UF160128'
        self.final_url = self.root_url + 'id=' + id + self.service_type + 'p=' + page + self.json + 'cb=setItemByidELMT' + id_ELMT
        '''

        self.utc_date = ''
        self.utc_hour = ''
        self.utc_min = ''

        self.path = path

    def get_current_utc_time(self):
        utc_now = datetime.datetime.utcnow()
        self.utc_date = str(utc_now.year) + str(utc_now.month).zfill(2) + str(utc_now.day).zfill(2)
        self.utc_hour = str(utc_now.hour).zfill(2)
        self.utc_min = str(utc_now.minute).zfill(2)

    def get_url(self, web_type, codes, page):
        url = ''
        if web_type == 0:
            url_format = self.formats[web_type]
            page = str(page)
            url = url_format['url'] + 'id=' + codes[0] + url_format['service_url'] + str(url_format['items']) \
                + '&p=' + page + url_format['json_cb'] + codes[1]
        return url

    def start_requests(self):
        for show in self.shows:
            codes = []
            show_title = show[0]
            codes.append(show[1])
            codes.append(show[2])
            section = show[3]
            url = self.get_url(show[4], codes, 1)
            self.get_current_utc_time()
            yield SplashRequest(
                url,
                self.parse,
                args={
                    'wait': 1.0,
                },
                meta={
                    'show_idx': self.shows.index(show),
                    'section': section,
                    'codes': codes,
                    'web_type': show[4],
                    'page': 1,
                }
            )

    def parse(self, response):
        show_idx = response.request.meta['show_idx']
        section = response.request.meta['section']
        codes = response.request.meta['codes']
        web_type = response.request.meta['web_type']
        page = response.request.meta['page']

        json_data = json.loads(response.body[42:-2])
        json_list = json_data.get('response').get('docs')
        page_list = []
        for item in json_list:
            title = item['videoTag'][1:-1]
            artist = item['videoTitle'].split(u'：')[1]
            url = item['videoUrl']
            page_list.append([title, artist, url])
            # TODO: Save as a file somewhere with page num - or download now
            print(title, artist, url)

        if page == 1:
            n_items = self.formats[web_type]['items']
            total_pages = int(ceil(float(json_data.get('response').get('numFound'))/n_items))
            for p_idx in range(2, total_pages + 1):
                url = self.get_url(web_type, codes, p_idx)
                yield SplashRequest(
                    url,
                    self.parse,
                    args={
                        'wait': 1.0,
                    },
                    meta={
                        'show_idx': show_idx,
                        'section': section,
                        'codes': codes,
                        'web_type': web_type,
                        'page': p_idx,
                    }
                )

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
