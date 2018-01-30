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
from yt_downloader import YoutubeDownloader


class CctvSpider(scrapy.Spider):
    name = "Cctv"

    def __init__(self, path):
        self.shows = [
            ['非常6+1', 'TOPC1451467940101208', '', '精彩看点', 14],
        ]

        self.formats = [
            {
                'url': 'http://api.cntv.cn/lanmu/videolistByColumnId?',
                'service_url': '&serviceId=tvcctv&type=1&n=',
                'items': 100,
                'json_cb': '&t=jsonp&cb=setItemByidELMT'
            },
            {
                'url': '',
            },
            {
                'url': '',
            },
            {
                'url': '',
            },
            {
                'url': '',
            },
            {
                'url': '',
            },
            {
                'url': '',
            },
            {
                'url': '',
            },
            {
                'url': '',
            },
            {
                'url': '',
            },
            {
                'url': '',
            },
            {
                'url': '',
            },
            {
                'url': '',
            },
            {
                'url': '',
            },
            {
                'url': 'http://api.cntv.cn/lanmu/videolistByColumnId?',
                'items': 100,
            },
        ]

        self.all_shows = [
            # 1 - ALL OK
            ['全球中文音乐榜上榜', 'TOPC1451542061864640', 'Y2oSEQdYWBBlMZCIG7UF160128', '精彩看点', 0],
            ['一起音乐吧', 'TOPC1451542132455743', 'Wko1T9K7rSHVc6q1rLNO160128', '精彩看点', 0],
            ['CCTV音乐厅', 'TOPC1451534421925242', 'JvrTH46rtYodBaNy2EAY160128', '精彩看点', 0],
            ['民歌·中国', 'TOPC1451541994820527', '6wZ1ivCiqkK3IdsDR7Ue160128', '精彩看点', 0],
            ['音乐传奇', 'TOPC1451542222069826', 'o14lfceelMrQgl1f4HJP160128', '精彩看点', 0],

            # 6 - ALL OK
            ['风华国乐', 'TOPC1451534503915324', 'Rd5X7WcB5FbgFfzQD4y1160128', '精彩看点', 0],
            ['精彩音乐汇', 'TOPC1451541414450906', 'ci3czCDkMCHn1Sm3GUYP160128', '精彩看点', 0],
            ['影视留声机', 'TOPC1451542346007956', 'aMYYOayXZUgOqOditFHk160128', '精彩看点', 0],
            ['中国音乐电视', 'TOPC1451542397206110', 'IJaYKRIupN0pxTX4cVlV160128', '精彩看点', 0],
            ['百年歌声', 'TOPC1451534465694290', 'IiqMS9z6W9gVhSwCAixq160127', '精彩看点', 0],

            # 11
            ['乐游天下', 'TOPC1451541538046196', 'e9hO43WpPk4DP4GH0LkF160128', '精彩看点', 0],  # OK
            ['我要上春晚', 'http://tv.cctv.com/lm/2017wyscw/', '', 'WHOLE PAGE', 1],           # OK
            ['星光大道', 'TOPC1451467630488780', 'KglXGa1D1WCZwhh4uaZ3160128', '精彩片段', 0],  # OK
            ['越战越勇', 'TOPC1451467829851129', 'A5DY1h2trsLm0RMGVjVY160206', '精彩片段', 0],  # OK
            ['回声嘹亮', 'TOPC1451535575561597', '', '精彩看点', 14], # TODO: OK/NOPE -> FALTA IR PASANDO DE AÑO Y MES Y PAGINA

            # 16
            ['幸福账单', 'TOPC1451535575561597', 'd6wx82jRexn0Qx8hoLFU160126', '精彩看点', 0],  # OK
            ['黄金100秒', 'http://tv.cctv.com/lm/hj100m/videoset/', '', 'WHOLE PAGE', 1],  # OK
            ['非常6+1', 'TOPC1451467940101208', '', '精彩看点', 14], # TODO: OK/NOPE -> FALTA IR PASANDO DE AÑO Y MES Y PAGINA
            ['综艺盛典', 'http://tv.cctv.com/lm/zysd/videoset/', '', 'WHOLE PAGE', 1],      # OK
            # ['天天把歌唱', '', '', 'ENTIRE SHOWS'],

            # 21 - ALL OK
            ['星光大道超级版', 'http://tv.cctv.com/lm/xgddcjb/video/index.shtml', '', 'WHOLE PAGE', 1],
            ['有朋远方来', 'http://tv.cctv.com/lm/ypyfl/videoset/', '', 'WHOLE PAGE', 1],
            ['中国正在听', 'http://tv.cctv.com/lm/zgzzt/videoset/', '', 'WHOLE PAGE', 1],
            ['完美星开幕', 'http://tv.cctv.com/lm/wmxkm/videoset/', '', 'WHOLE PAGE', 1],
            ['巅峰音乐汇', 'http://tv.cctv.com/lm/dfyyh/videoset/', '', 'WHOLE PAGE', 2],

            # 26
            ['“中国梦”主题歌曲展播', 'http://ent.cntv.cn/special/zgmgqz/', '', 'WHOLE PAGE', 3],     # OK
            ['中国民歌大会第二季', 'http://tv.cctv.com/cctv3/special/2017mgdh/index.shtml', '', '视频回顾', 4], # TODO: NOPE! JAVASCRIPT PROBLEM
            ['我和我的祖国2017', 'http://music.cctv.com/special/whwdzg2017/index.shtml', '', 'WHOLE PAGE', 5], # OK
            ['2017年中秋晚会', 'http://tv.cctv.com/2017/09/21/VIDAuTggsVYiMmLnOgLnPKDB170921.shtml', '', '精彩看点', 6], # TODO: NOPE! JAVASCRIPT PROBLEM
            ['中秋特别节目', 'http://tv.cctv.com/cctv3/special/2017wjymy/index.shtml', '', 'WHOLE PAGE', 1], # OK

            # 31
            ['江山如画-2017国庆音乐会', 'http://music.cctv.com/special/2017jsrh/index.shtml', '', '精彩视频', 7], # OK
            ['中国梦 祖国颂2017', 'http://tv.cctv.com/2017/09/26/VIDAGMO9c7wSn9PNgP88nv8F170926.shtml', '', '精彩看点', 6], # TODO: NOPE! JAVASCRIPT PROBLEM
            ['强军战旗红——建军90周年“心连心”赴南昌慰问演出', 'http://tv.cctv.com/2017/07/31/VIDAyJUXRTNc4saRFK5YLKvk170731.shtml', '', '精彩看点', 6], # TODO: NOPE! JAVASCRIPT PROBLEM
            ['在党的旗帜下', 'http://tv.cctv.com/2017/08/01/VIDA9KMlXxaLT4axj4rOHwVO170801.shtml', '', '精彩看点', 6],  # TODO: NOPE! JAVASCRIPT PROBLEM
            ['守望相助草原情', 'http://tv.cctv.com/2017/08/08/VIDA2ZoXCZt81FsrgXB1yi1y170808.shtml', '', '精彩看点', 6], # TODO: NOPE! JAVASCRIPT PROBLEM

            # 36 - ALL OK
            ['歌声飘过90年', 'http://ent.cctv.com/special/90/01/index.shtml', '', 'WHOLE PAGE', 8],
            ['唱支山歌给党听', 'http://music.cctv.com/special/2017czsggdt/', '', 'WHOLE PAGE', 5],
            ['山水寄美端午情', 'http://ent.cctv.com/special/dw/index.shtml', '', 'WHOLE PAGE', 1],
            ['中国梦·劳动美2017', 'http://ent.cctv.com/special/xlx/index.shtml', '', 'WHOLE PAGE', 5],
            ['2017春晚', 'http://chunwan.cctv.com/', '', 'WHOLE PAGE', 9],

            # 41
            ['美丽中国唱起来', 'http://tv.cctv.com/2017/01/19/VIDALucOxtJEnqZCSSJtV9WP170119.shtml', '', '精彩看点', 6], # TODO: NOPE! JAVASCRIPT PROBLEM
            ['启航2017', 'http://music.cctv.com/special/qihang2017/index.shtml', '', 'WHOLE PAGE', 7], # OK
            ['我和我的祖国2016', 'http://music.cctv.com/special/2016gq/index.shtml', '', 'WHOLE PAGE', 7], # OK
            ['中国梦 祖国颂2016', 'http://tv.cctv.com/cctv3/2016gqwh/db/index.shtml', '', 'WHOLE PAGE', 1], # OK
            ['中国民歌大会第一季', 'http://tv.cctv.com/cctv3/zgmgdh/index.shtml', '', '视频回顾', 10], # OK

            # 46
            # ['寻找刘三姐第三季', '', '', 'ENTIRE SHOWS'],
            ['心连心艺术团慰问演出', 'http://tv.cntv.cn/videoset/C19548/page/1', '', '精彩片段', 13], # TODO: OK/NOPE -> FALTA NEXT PAGE
            ['伟大的旗帜', 'http://tv.cctv.com/cctv3/wddqz/index.shtml', '', 'WHOLE PAGE', 1], # OK
            ['中国梦·劳动美2016', 'http://tv.cctv.com/cctv3/51wh/index.shtml', '', 'WHOLE PAGE', 1], # OK
            ['2016春晚', 'http://chunwan.cntv.cn/2016/index.shtml', '', 'WHOLE PAGE', 11], # OK

            # 51
            ['启航2016', 'http://ent.cntv.cn/special/qihang/2016/index.shtml', '', 'WHOLE PAGE', 5], # TODO: NOPE! JAVASCRIPT !
            ['2015春晚', 'http://chunwan.cntv.cn/2015/', '', 'WHOLE PAGE', 1], # OK
            ['胜利与和平', 'http://ent.cntv.cn/special/slyhp/', '', 'WHOLE PAGE', 12], # OK
            ['中国好歌曲第三季', 'TOPC1451984949453678', 'uRiql41hi1BNW0BX3xfB160128', '精彩片段', 0], # OK
            ['中国好歌曲第二季', 'http://tv.cctv.com/lm/zghgq2/videoset/', '', 'WHOLE PAGE', 1], # OK

            # 56
            ['中国好歌曲', 'http://tv.cntv.cn/videoset/VSET100181076033', '', '精彩片段', 13], # TODO: OK/NOPE -> FALTA NEXT PAGE
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

    def get_url(self, web_type, codes, page):
        url = ''
        url_format = self.formats[web_type]
        if web_type == 0:
            page = str(page)
            url = url_format['url'] + 'id=' + codes[0] + url_format['service_url'] + str(url_format['items']) \
                + '&p=' + page + url_format['json_cb'] + codes[1]
        elif web_type == 1 or web_type == 2 or web_type == 3 or web_type == 4 or web_type == 5 or web_type == 6 \
                or web_type == 7 or web_type == 8 or web_type == 9 or web_type == 10 or web_type == 11 \
                or web_type == 12 or web_type == 13:
            url = codes[0]
        elif web_type == 14:
            page = str(page)
            year = 2017
            month = 12
            url = url_format['url'] + 'id=' + codes[0] + '&n=' + str(url_format['items']) + '&of=fdate&p=' + page \
                + '&type=1&serviceId=tvcctv' + '&Y=' + str(year) + '&M=' + str(month)
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

    def parse_0(self, response):
        show_idx = response.request.meta['show_idx']
        section = response.request.meta['section']
        codes = response.request.meta['codes']
        web_type = response.request.meta['web_type']
        page = response.request.meta['page']

        json_data = json.loads(response.body[42:-2])
        json_list = json_data.get('response').get('docs')
        page_list = []
        for item in json_list:
            if codes[0] != 'TOPC1451984949453678':
                title = item['videoTag'][1:-1]
            else:
                title = item['videoTitle']
            artist = item['videoTitle'].split(u'：')[1]
            url = item['videoUrl']
            # yt_downloader = YoutubeDownloader()
            # track_info = artist + ' - ' + title
            # yt_downloader.download(url, self.path, track_info)
            page_list.append([title, artist, url])
            # TODO: Save as a file somewhere with page num - or download now
            print(title, artist, url)

        if page == 1:
            n_items = self.formats[web_type]['items']
            total_pages = int(ceil(float(json_data.get('response').get('numFound')) / n_items))
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

    def parse_1(self, response, web_type):
        if web_type == 1 or web_type == 2 or web_type == 11:
            titles = response.xpath(".//div[@class='image_list_box']//ul//div[@class='text']//a/text()").extract()
            urls = response.xpath(".//div[@class='image_list_box']//ul//div[@class='text']//a/@href").extract()
            if web_type == 11:
                urls_ = urls
                urls = []
                for url in urls_:
                    if u'download.cntv.cn' not in url:
                        urls.append(url)
        elif web_type == 5:
            titles = response.xpath(".//div[@class='image_list_box_zdy']//ul[@class='il_w120_b1 video_plus']//div[@class='text']//a/text()").extract()
            urls = response.xpath(".//div[@class='image_list_box_zdy']//ul[@class='il_w120_b1 video_plus']//div[@class='text']//a/@href").extract()
            len_discard = len(titles) - len(urls)
            titles = titles[len_discard*2:]
            urls = urls[len_discard:]
        elif web_type == 6:
            # TODO: Javascript problem, pestañitas
            print('st')
        elif web_type == 7:
            titles = response.xpath(".//div[@class='image_list_box_zdy']//ul[@class='il_w120_b1  ']//div[@class='text']//a/text()").extract()
            urls = response.xpath(".//div[@class='image_list_box_zdy']//ul[@class='il_w120_b1  ']//div[@class='text']//a/@href").extract()
        elif web_type == 8:
            titles = response.xpath(".//div[@class='image_list_box_zdy']//ul[@class='il_w120_b1 video_plus']//div[@class='text']//a/text()").extract()
            urls = response.xpath(".//div[@class='image_list_box_zdy']//ul[@class='il_w120_b1 video_plus']//div[@class='text']//a/@href").extract()
            titles += response.xpath(".//div[@class='image_list_box']//ul[@class='il_w120_b1 video_plus']//div[@class='text']//a/text()").extract()
            urls += response.xpath(".//div[@class='image_list_box']//ul[@class='il_w120_b1 video_plus']//div[@class='text']//a/@href").extract()
        elif web_type == 9:
            titles = response.xpath(".//div[@class='chunwan16252_con03']//ul//li//div[@class='text']//a/text()").extract()
            urls = response.xpath(".//div[@class='chunwan16252_con03']//ul//li//div[@class='text']//a/@href").extract()
        elif web_type == 10:
            titles = response.xpath(".//div[@class='bottom_con']//ul//li//p//a/text()").extract()
            urls = response.xpath(".//div[@class='bottom_con']//ul//li//p//a/@href").extract()
        elif web_type == 12:
            titles = response.xpath(".//div[@class='box_right']//div[@class='image_lt']//div[@class='text']//a/text()").extract()
            titles += response.xpath(".//div[@class='box_right']//div[@class='image_lt02']//div[@class='text']//a/text()").extract()
            urls = response.xpath(".//div[@class='box_right']//div[@class='image_lt']//div[@class='text']//a/@href").extract()
            urls += response.xpath(".//div[@class='box_right']//div[@class='image_lt02']//div[@class='text']//a/@href").extract()
        elif web_type == 13:
            titles = response.xpath(".//div[@class='md_bd']//div[@class='image_list']//h3//a/text()").extract()
            urls = response.xpath(".//div[@class='md_bd']//div[@class='image_list']//h3//a/@href").extract()
            # TODO: GO TO NEXT PAGE
        tracks = []
        for item in titles:
            if u'《' in item:
                if (web_type == 1 or web_type == 5 or web_type == 7 or web_type == 8 or web_type == 9) \
                        and u'：' in item:
                    title = item[item.find(u'《')+1:item.find(u'》')]
                    artist = item.split(u'：')[1]
                    url = urls[titles.index(item)]
                    tracks.append([title, artist, url])
                elif web_type == 2:
                    title = item[item.find(u'《') + 1:item.find(u'》')]
                    artist = item.split(u'》')[1]
                    url = urls[titles.index(item)]
                    tracks.append([title, artist, url])
                elif web_type == 12:
                    title = item[item.find(u'《')+1:item.find(u'》')]
                    artist = 'N/A'
                    url = urls[titles.index(item)]
                    tracks.append([title, artist, url])

    def parse_3(self, response, web_type):
        titles_raw = response.xpath(".//div[@class='image_list_box']//ul//div[@class='text']//a")
        urls = response.xpath(".//div[@class='image_list_box']//ul//div[@class='text']//a/@href").extract()
        tracks = []
        for item in titles_raw:
            title_raw = item.xpath(".//text()").extract()
            if len(title_raw) > 1:
                if u'《' in title_raw[0]:
                    title = title_raw[0][title_raw[0].find(u'《')+1:title_raw[0].find(u'》')]
                    if u'：' in title_raw[1]:
                        artist = title_raw[1].split(u'：')[1]
                        if len(title_raw) == 3:
                            artist += ' ' + title_raw[2]
                        url = urls[titles_raw.index(item)]
                        tracks.append([title, artist, url])

    def parse_4(self, response, web_type):
        # TODO: Javascript problem, the singles section is entirely depending on that (8 subsections)
        print('sth')

    def parse(self, response):
        web_type = response.request.meta['web_type']
        if web_type == 0 or web_type == 14:
            show_idx = response.request.meta['show_idx']
            section = response.request.meta['section']
            codes = response.request.meta['codes']
            web_type = response.request.meta['web_type']
            page = response.request.meta['page']

            if web_type == 0:
                json_data = json.loads(response.body[42:-2])
                json_list = json_data.get('response').get('docs')
            elif web_type == 14:
                json_data = json.loads(response.body)
                json_list = json_data.get('response').get('docs')
            page_list = []
            for item in json_list:
                title = ''
                artist = ''
                if codes[0] == 'TOPC1451984949453678' or codes[0] == 'TOPC1451535575561597' \
                        or codes[0] == 'TOPC1451467940101208':
                    if u'《' in item['videoTitle']:
                        title = item['videoTitle'][item['videoTitle'].find(u'《')+1:item['videoTitle'].find(u'》')]
                else:
                    title = item['videoTag'][1:-1]
                if u'：' in item['videoTitle']:
                    artist = item['videoTitle'].split(u'：')[1]
                if title != '' and artist != '':
                    url = item['videoUrl']
                    # yt_downloader = YoutubeDownloader()
                    # track_info = artist + ' - ' + title
                    # yt_downloader.download(url, self.path, track_info)
                    page_list.append([title, artist, url])
                # TODO: Save as a file somewhere with page num - or download now

            if page == 1:
                n_items = self.formats[web_type]['items']
                total_pages = int(ceil(float(json_data.get('response').get('numFound')) / n_items))
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
        elif web_type == 1 or web_type == 2 or web_type == 5 or web_type == 6 or web_type == 7 or web_type == 8 \
                or web_type == 9 or web_type == 10 or web_type == 11 or web_type == 12 or web_type == 13:
            self.parse_1(response, web_type)
        elif web_type == 3:
            self.parse_3(response, web_type)
        elif web_type == 4:
            self.parse_4(response, web_type)

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
