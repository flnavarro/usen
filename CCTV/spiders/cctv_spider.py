# -*- coding: utf-8 -*-
import os
import scrapy
import xlwt
import xlrd
import datetime
import json
import ast
from math import ceil


class CctvSpider(scrapy.Spider):
    name = "Cctv"

    def __init__(self, path, first_execution):
        self.path = path + 'shows/'
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        self.shows = [
            ['01 全球中文音乐榜上榜', 'TOPC1451542061864640', 'Y2oSEQdYWBBlMZCIG7UF160128', '精彩看点', 0, False],
            ['02 一起音乐吧', 'TOPC1451542132455743', 'Wko1T9K7rSHVc6q1rLNO160128', '精彩看点', 0, False],
            ['03 CCTV音乐厅', 'TOPC1451534421925242', 'JvrTH46rtYodBaNy2EAY160128', '精彩看点', 0, False],
            ['04 民歌·中国', 'TOPC1451541994820527', '6wZ1ivCiqkK3IdsDR7Ue160128', '精彩看点', 0, False],
            ['05 音乐传奇', 'TOPC1451542222069826', 'o14lfceelMrQgl1f4HJP160128', '精彩看点', 0, False],
            ['06 风华国乐', 'TOPC1451534503915324', 'Rd5X7WcB5FbgFfzQD4y1160128', '精彩看点', 0, False],
            ['07 精彩音乐汇', 'TOPC1451541414450906', 'ci3czCDkMCHn1Sm3GUYP160128', '精彩看点', 0, False],
            ['08 影视留声机', 'TOPC1451542346007956', 'aMYYOayXZUgOqOditFHk160128', '精彩看点', 0, False],
            ['09 中国音乐电视', 'TOPC1451542397206110', 'IJaYKRIupN0pxTX4cVlV160128', '精彩看点', 0, False],
            ['10 百年歌声', 'TOPC1451534465694290', 'IiqMS9z6W9gVhSwCAixq160127', '精彩看点', 0, True],
            ['11 乐游天下', 'TOPC1451541538046196', 'e9hO43WpPk4DP4GH0LkF160128', '精彩看点', 0, False],
            ['12 我要上春晚', 'http://tv.cctv.com/lm/2017wyscw/', '', 'WHOLE PAGE', 1, False],
            ['13 星光大道', 'TOPC1451467630488780', 'KglXGa1D1WCZwhh4uaZ3160128', '精彩片段', 0, False],
            ['14 越战越勇', 'TOPC1451467829851129', 'A5DY1h2trsLm0RMGVjVY160206', '精彩片段', 0, False],
            ['15 回声嘹亮', 'TOPC1451535575561597', '', '精彩看点', 14, False],
            ['16 幸福账单', 'TOPC1451535575561597', 'd6wx82jRexn0Qx8hoLFU160126', '精彩看点', 0, False],
            ['17 黄金100秒', 'http://tv.cctv.com/lm/hj100m/videoset/', '', 'WHOLE PAGE', 1, False],
            ['18 非常6+1', 'TOPC1451467940101208', '', '精彩看点', 14, False],
            ['19 综艺盛典', 'http://tv.cctv.com/lm/zysd/videoset/', '', 'WHOLE PAGE', 1, False],
            # ['20 天天把歌唱', '', '', 'ENTIRE SHOWS', False],
            ['21 星光大道超级版', 'http://tv.cctv.com/lm/xgddcjb/video/index.shtml', '', 'WHOLE PAGE', 1, False],
            ['22 有朋远方来', 'http://tv.cctv.com/lm/ypyfl/videoset/', '', 'WHOLE PAGE', 1, False],
            ['23 中国正在听', 'http://tv.cctv.com/lm/zgzzt/videoset/', '', 'WHOLE PAGE', 1, True],
            ['24 完美星开幕', 'http://tv.cctv.com/lm/wmxkm/videoset/', '', 'WHOLE PAGE', 1, True],
            ['25 巅峰音乐汇', 'http://tv.cctv.com/lm/dfyyh/videoset/', '', 'WHOLE PAGE', 2, True],
            ['26 “中国梦”主题歌曲展播', 'http://ent.cntv.cn/special/zgmgqz/', '', 'WHOLE PAGE', 3, False],
            ['27 中国民歌大会第二季', 'http://tv.cctv.com/cctv3/special/2017mgdh/bhy/', '', '视频回顾', 4, False],
            ['28 我和我的祖国2017', 'http://music.cctv.com/special/whwdzg2017/index.shtml', '', 'WHOLE PAGE', 5, False],
            ['29 2017年中秋晚会', 'http://tv.cctv.com/2017/09/21/VIDAuTggsVYiMmLnOgLnPKDB170921.shtml', '', '精彩看点', 6, True],
            ['30 中秋特别节目', 'http://tv.cctv.com/cctv3/special/2017wjymy/index.shtml', '', 'WHOLE PAGE', 1, True],
            ['31 江山如画-2017国庆音乐会', 'http://music.cctv.com/special/2017jsrh/index.shtml', '', '精彩视频', 7, True],
            ['32 中国梦 祖国颂2017', 'http://tv.cctv.com/2017/09/26/VIDAGMO9c7wSn9PNgP88nv8F170926.shtml', '', '精彩看点', 6,
             True],
            ['33 强军战旗红——建军90周年“心连心”赴南昌慰问演出', 'http://tv.cctv.com/2017/07/31/VIDAyJUXRTNc4saRFK5YLKvk170731.shtml', '',
             '精彩看点', 6, True],
            ['34 在党的旗帜下', 'http://tv.cctv.com/2017/08/01/VIDA9KMlXxaLT4axj4rOHwVO170801.shtml', '', '精彩看点', 6, True],
            ['35 守望相助草原情', 'http://tv.cctv.com/2017/08/08/VIDA2ZoXCZt81FsrgXB1yi1y170808.shtml', '', '精彩看点', 6, True],
            ['36 歌声飘过90年', 'http://ent.cctv.com/special/90/01/index.shtml', '', 'WHOLE PAGE', 8, True],
            ['37 唱支山歌给党听', 'http://music.cctv.com/special/2017czsggdt/', '', 'WHOLE PAGE', 5, True],
            ['38 山水寄美端午情', 'http://ent.cctv.com/special/dw/index.shtml', '', 'WHOLE PAGE', 1, True],
            ['39 中国梦·劳动美2017', 'http://ent.cctv.com/special/xlx/index.shtml', '', 'WHOLE PAGE', 5, True],
            ['40 2017春晚', 'http://chunwan.cctv.com/', '', 'WHOLE PAGE', 9, True],
            ['41 美丽中国唱起来', 'http://tv.cctv.com/2017/01/19/VIDALucOxtJEnqZCSSJtV9WP170119.shtml', '', '精彩看点', 6, True],
            ['42 启航2017', 'http://music.cctv.com/special/qihang2017/index.shtml', '', 'WHOLE PAGE', 7, True],
            ['43 我和我的祖国2016', 'http://music.cctv.com/special/2016gq/index.shtml', '', 'WHOLE PAGE', 7, True],
            ['44 中国梦 祖国颂2016', 'http://tv.cctv.com/cctv3/2016gqwh/db/index.shtml', '', 'WHOLE PAGE', 1, True],
            ['45 中国民歌大会第一季', 'http://tv.cctv.com/cctv3/zgmgdh/index.shtml', '', '视频回顾', 10, True],
            # ['46 寻找刘三姐第三季', '', '', 'ENTIRE SHOWS', True],
            ['47 心连心艺术团慰问演出', 'C19548', '', '精彩片段', 13, False],
            ['48 伟大的旗帜', 'http://tv.cctv.com/cctv3/wddqz/index.shtml', '', 'WHOLE PAGE', 1, True],
            ['49 中国梦·劳动美2016', 'http://tv.cctv.com/cctv3/51wh/index.shtml', '', 'WHOLE PAGE', 1, True],
            ['50 2016春晚', 'http://chunwan.cntv.cn/2016/index.shtml', '', 'WHOLE PAGE', 11, True],
            ['51 启航2016', 'VSET100257115724', '', 'WHOLE PAGE', 15, True],
            ['52 2015春晚', 'http://chunwan.cntv.cn/2015/', '', 'WHOLE PAGE', 1, True],
            # ['53 胜利与和平', 'http://ent.cntv.cn/special/slyhp/', '', 'WHOLE PAGE', 12, True],
            ['54 中国好歌曲第三季', 'TOPC1451984949453678', 'uRiql41hi1BNW0BX3xfB160128', '精彩片段', 0, True],
            ['55 中国好歌曲第二季', 'http://tv.cctv.com/lm/zghgq2/videoset/', '', 'WHOLE PAGE', 1, True],
            ['56 中国好歌曲', 'VSET100181076033', '', '精彩片段', 13, True],
        ]

        # self.shows = [
        #     ['29 2017年中秋晚会', 'http://tv.cctv.com/2017/09/21/VIDAuTggsVYiMmLnOgLnPKDB170921.shtml', '', '精彩看点', 6, True],
        # ]

        self.first_execution = first_execution

        self.api_data = {
            'url': 'http://api.cntv.cn/lanmu/videolistByColumnId?',
            'service_url': '&serviceId=tvcctv&type=1&n=',
            'items': 100,
            'json_cb': '&t=jsonp&cb=setItemByidELMT'
        }
        self.year_now = str(datetime.datetime.utcnow().year)

    def get_url(self, web_type, codes, page):
        url = ''
        page = str(page)
        if web_type == 0:
            url = self.api_data['url'] + 'id=' + codes[0] + self.api_data['service_url'] \
                + str(self.api_data['items']) + '&p=' + page + self.api_data['json_cb'] + codes[1]
        elif web_type == 1 or web_type == 2 or web_type == 3 or web_type == 5 or web_type == 6 \
                or web_type == 7 or web_type == 8 or web_type == 9 or web_type == 10 or web_type == 11 \
                or web_type == 12:
            url = codes[0]
        elif web_type == 4:
            page_code = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth']
            url = codes[0] + page_code[int(page) - 1] + '/index.shtml'
        elif web_type == 13:
            url = 'http://tv.cntv.cn/index.php?action=videoset-videolistbytype&class=lanmu&page=' + page \
                  + '&setid=' + codes[0] + '&istiyu=0'
        elif web_type == 14:
            url = self.api_data['url'] + 'id=' + codes[0] + '&n=' + str(self.api_data['items']) \
                + '&of=fdate&p=' + page + '&type=1&serviceId=tvcctv'
        elif web_type == 15:
            url = 'http://api.cntv.cn/video/videolistById?vsid=' + codes[0] + '&serviceId=channel' \
                + '&of=time&em=2&o=desc&n=100&cb=callbackfun&t=jsonp' + '&p=' + page
        return url

    def start_requests(self):
        for show in self.shows:
            if (not self.first_execution and not show[5]) or self.first_execution:
                codes = []
                show_title = show[0]
                codes.append(show[1])
                codes.append(show[2])
                section = show[3]
                url = self.get_url(show[4], codes, 1)
                yield scrapy.Request(
                    url=url,
                    callback=self.parse,
                    errback=self.parse_error,
                    meta={
                        'show_title': show_title,
                        'section': section,
                        'codes': codes,
                        'web_type': show[4],
                        'page': 1,
                    }
                )

    def parse_single_page(self, response, web_type):
        titles = []
        titles_3_raw = []
        urls = []
        if web_type == 1 or web_type == 2 or web_type == 11:
            titles = response.xpath(".//div[@class='image_list_box']//ul//div[@class='text']//a/text()").extract()
            urls = response.xpath(".//div[@class='image_list_box']//ul//div[@class='text']//a/@href").extract()
            if web_type == 11:
                urls_ = urls
                urls = []
                for url in urls_:
                    if u'download.cntv.cn' not in url:
                        urls.append(url)
        elif web_type == 3:
            titles_ = response.xpath(".//div[@class='image_list_box']//ul//div[@class='text']//a")
            for item in titles_:
                titles_3_raw.append(item.xpath(".//text()").extract())
                titles.append(item.xpath(".//text()").extract_first())
            urls = response.xpath(".//div[@class='image_list_box']//ul//div[@class='text']//a/@href").extract()
        elif web_type == 5:
            titles = response.xpath(".//div[@class='image_list_box_zdy']//ul[@class='il_w120_b1 video_plus']//div[@class='text']//a/text()").extract()
            urls = response.xpath(".//div[@class='image_list_box_zdy']//ul[@class='il_w120_b1 video_plus']//div[@class='text']//a/@href").extract()
            len_discard = len(titles) - len(urls)
            titles = titles[len_discard*2:]
            urls = urls[len_discard:]
        elif web_type == 6:
            json_raw = response.xpath(".//script[@type='text/javascript']/text()").extract()
            for item_raw in json_raw:
                if u'jsonData2=' in item_raw:
                    data_raw = item_raw[item_raw.find('jsonData2=') + len('jsonData2=') + 1:]
                    data_raw = data_raw[:data_raw.find('];')].replace(' ', '').replace('\r', '').replace('\n', '')
                    json_list = ast.literal_eval(data_raw)
                    for item in json_list:
                        titles.append(item['title'].decode('utf-8'))
                        urls.append(item['url'])
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
        tracks = []
        idx = 1
        for item in titles:
            artist = ''
            if u'《' in item and u'》' in item:
                title = item[item.find(u'《') + 1:item.find(u'》')]
                if (web_type == 1 or web_type == 5 or web_type == 6 or web_type == 7 or web_type == 8
                        or web_type == 9 or web_type == 10 or web_type == 11) and u'：' in item:
                    artist = item.split(u'：')[1]
                elif web_type == 2:
                    artist = item.split(u'》')[1]
                elif web_type == 3:
                    t3_id = titles.index(item)
                    if u'：' in titles_3_raw[t3_id][1]:
                        artist = titles_3_raw[t3_id][1].split(u'：')[1]
                        if len(titles_3_raw[t3_id]) == 3:
                            artist += ' ' + titles_3_raw[t3_id][2]
                elif web_type == 12:
                    artist = 'N/A'
                if artist != '':
                    url = urls[titles.index(item)]
                    tracks.append({
                        'title': title,
                        'artist': artist,
                        'url': url,
                        'index': idx
                    })
                    idx += 1
        show_title = response.request.meta['show_title']
        self.save_list(tracks, show_title, 1)

    def parse(self, response):
        web_type = response.request.meta['web_type']
        show_title = response.request.meta['show_title']
        section = response.request.meta['section']
        codes = response.request.meta['codes']
        page = response.request.meta['page']

        if web_type == 0 or web_type == 14 or web_type == 15:
            if web_type == 0:
                json_data = json.loads(response.body[42:-2])
                json_list = json_data.get('response').get('docs')
            elif web_type == 14:
                json_data = json.loads(response.body)
                json_list = json_data.get('response').get('docs')
            elif web_type == 15:
                json_data = json.loads(response.body[12:-2])
                json_list = json_data.get('video')
            page_list = []
            row = 1
            for item in json_list:
                video_title = ''
                title = ''
                artist = ''
                url = ''
                if web_type == 0 or web_type == 14:
                    video_title = item['videoTitle']
                    url = item['videoUrl']
                elif web_type == 15:
                    video_title = item['t']
                    url = item['url']
                if u'《' in video_title and u'》' in video_title:
                    title = video_title[video_title.find(u'《') + 1:video_title.find(u'》')]
                if u'：' in video_title:
                    artist = video_title.split(u'：')[1]
                if title != '' and artist != '':
                    page_list.append({
                        'title': title,
                        'artist': artist,
                        'url': url,
                        'index': row + (page - 1) * self.api_data['items'],
                    })
                row += 1
            self.save_list(page_list, show_title, page)

            if page == 1:
                n_items = self.api_data['items']
                total_pages = 1
                if web_type == 0 or web_type == 14:
                    total_pages = int(ceil(float(json_data.get('response').get('numFound')) / n_items))
                elif web_type == 15:
                    total_pages = int(ceil(float(json_data.get('videoset').get('count')) / n_items))
                if total_pages > 1:
                    page_limit = total_pages + 1
                    for p_idx in range(2, page_limit):
                        url = self.get_url(web_type, codes, p_idx)
                        yield scrapy.Request(
                            url=url,
                            callback=self.parse,
                            errback=self.parse_error,
                            meta={
                                'show_title': show_title,
                                'section': section,
                                'codes': codes,
                                'web_type': web_type,
                                'page': p_idx,
                            }
                        )

        elif web_type == 1 or web_type == 2 or web_type == 3 or web_type == 5 or web_type == 6 or web_type == 7 \
                or web_type == 8 or web_type == 9 or web_type == 10 or web_type == 11 \
                or web_type == 12:
            self.parse_single_page(response, web_type)

        elif web_type == 4 or web_type == 13:
            titles = ''
            urls = ''
            items_per_page = 1
            if web_type == 4:
                titles = response.xpath("..//li//p//a/text()").extract()
                urls = response.xpath("..//li//p//a/@href").extract()
                items_per_page = 20
            elif web_type == 13:
                titles = response.xpath(".//div[@class='md_bd']//div[@class='image_list']//h3//a/text()").extract()
                urls = response.xpath(".//div[@class='md_bd']//div[@class='image_list']//h3//a/@href").extract()
                items_per_page = 12

            tracks = []
            idx = 1
            for item in titles:
                artist = ''
                if u'《' in item and u'》' in item:
                    title = item[item.find(u'《') + 1:item.find(u'》')]
                    if u'：' in item:
                        artist = item.split(u'：')[1]
                    if artist != '':
                        url = urls[titles.index(item)]
                        tracks.append({
                            'title': title,
                            'artist': artist,
                            'url': url,
                            'index': idx + (page - 1) * items_per_page
                        })
                        idx += 1

            self.save_list(tracks, show_title, page)

            if (web_type == 4 and page < 8) or (web_type == 13 and len(titles) == 12):
                url = self.get_url(web_type, codes, page + 1)
                yield scrapy.Request(
                    url=url,
                    callback=self.parse,
                    errback=self.parse_error,
                    meta={
                        'show_title': show_title,
                        'section': section,
                        'codes': codes,
                        'web_type': web_type,
                        'page': page + 1,
                    }
                )

    def save_list(self, track_list, show_title, page):
        if os.path.exists(self.path):
            folder_path = self.path + show_title
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            if page == 1:
                checkfile_path = folder_path + '/' + 'last_tracks_candidates.xls'
                max_list = 10
                if len(track_list) < 10:
                    max_list = len(track_list)
                last_tracks = track_list[:max_list]
                lt_xls = xlwt.Workbook()
                sheet = lt_xls.add_sheet(show_title.decode('utf-8'))
                sheet.write(0, 0, 'Track Title')
                sheet.write(0, 1, 'Track Artist')
                sheet.write(0, 2, 'Track URL')
                row = 1
                for track in last_tracks:
                    sheet.write(row, 0, track['title'])
                    sheet.write(row, 1, track['artist'])
                    sheet.write(row, 2, track['url'])
                    row += 1
                lt_xls.save(checkfile_path)
            file_path = folder_path + '/' + 'tracks_to_download.xls'
            tracks_to_dl = []
            if os.path.exists(file_path):
                xls = xlrd.open_workbook(file_path, formatting_info=True)
                n_rows = xls.sheet_by_index(0).nrows
                sheet_read = xls.sheet_by_index(0)
                for row in range(1, n_rows):
                    title = sheet_read.cell(row, 0).value
                    artist = sheet_read.cell(row, 1).value
                    url = sheet_read.cell(row, 2).value
                    dl_idx = sheet_read.cell(row, 3).value
                    tracks_to_dl.append({
                        'title': title,
                        'artist': artist,
                        'url': url,
                        'index': dl_idx,
                    })
            tracks_to_dl += track_list
            list_xls = xlwt.Workbook()
            sheet = list_xls.add_sheet(show_title.decode('utf-8'))
            sheet.write(0, 0, 'Track Title')
            sheet.write(0, 1, 'Track Artist')
            sheet.write(0, 2, 'Track URL')
            sheet.write(0, 3, 'Download Index')
            row = 1
            for track in tracks_to_dl:
                sheet.write(row, 0, track['title'])
                sheet.write(row, 1, track['artist'])
                sheet.write(row, 2, track['url'])
                sheet.write(row, 3, track['index'])
                row += 1
            list_xls.save(file_path)
        else:
            print('The path specified does not exist')

    def parse_error(self, response):
        print('There was a response error of type -> ' + response.value.response.status)
