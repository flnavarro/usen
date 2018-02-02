# -*- coding: utf-8 -*-
from yt_downloader import YoutubeDownloader
from metadata_manager import MetadataManager
import time
import os
import logging
import xlwt
import xlrd


class Track(object):
    def __init__(self, artist, title, show, cctv_url):
        self.artist = artist
        self.title = title
        self.show = show
        self.cctv_url = cctv_url


class BatchManager(object):
    def __init__(self, n_tracks_per_batch, batches_path, first_execution):
        self.yt_downloader = YoutubeDownloader()
        self.metadata = MetadataManager()

        self.n_tracks_per_batch = n_tracks_per_batch
        self.batches_path = batches_path

        self.current_batch_number = 1
        self.current_batch_size = 0
        self.current_batch_name = ''
        self.current_batch_path = ''
        self.tracks_path = ''
        self.date = ''
        self.date_previous_batch = ''
        self.create_batch()

        self.global_log = None
        self.open_global_log()
        self.current_batch_log = None

        self.tracks_dl_list = []

        self.first_execution = first_execution

        self.shows = [
            ['01 全球中文音乐榜上榜', 'TOPC1451542061864640', 'Y2oSEQdYWBBlMZCIG7UF160128', '精彩看点', 0, False],
            ['15 回声嘹亮', 'TOPC1451535575561597', '', '精彩看点', 14, False],
        ]

        # self.shows = [
        #     ['01 全球中文音乐榜上榜', 'TOPC1451542061864640', 'Y2oSEQdYWBBlMZCIG7UF160128', '精彩看点', 0, False],
        #     ['02 一起音乐吧', 'TOPC1451542132455743', 'Wko1T9K7rSHVc6q1rLNO160128', '精彩看点', 0, False],
        #     ['03 CCTV音乐厅', 'TOPC1451534421925242', 'JvrTH46rtYodBaNy2EAY160128', '精彩看点', 0, False],
        #     ['04 民歌·中国', 'TOPC1451541994820527', '6wZ1ivCiqkK3IdsDR7Ue160128', '精彩看点', 0, False],
        #     ['05 音乐传奇', 'TOPC1451542222069826', 'o14lfceelMrQgl1f4HJP160128', '精彩看点', 0, False],
        #     ['06 风华国乐', 'TOPC1451534503915324', 'Rd5X7WcB5FbgFfzQD4y1160128', '精彩看点', 0, False],
        #     ['07 精彩音乐汇', 'TOPC1451541414450906', 'ci3czCDkMCHn1Sm3GUYP160128', '精彩看点', 0, False],
        #     ['08 影视留声机', 'TOPC1451542346007956', 'aMYYOayXZUgOqOditFHk160128', '精彩看点', 0, False],
        #     ['09 中国音乐电视', 'TOPC1451542397206110', 'IJaYKRIupN0pxTX4cVlV160128', '精彩看点', 0, False],
        #     ['10 百年歌声', 'TOPC1451534465694290', 'IiqMS9z6W9gVhSwCAixq160127', '精彩看点', 0, True],
        #     ['11 乐游天下', 'TOPC1451541538046196', 'e9hO43WpPk4DP4GH0LkF160128', '精彩看点', 0, False],
        #     ['12 我要上春晚', 'http://tv.cctv.com/lm/2017wyscw/', '', 'WHOLE PAGE', 1, False],
        #     ['13 星光大道', 'TOPC1451467630488780', 'KglXGa1D1WCZwhh4uaZ3160128', '精彩片段', 0, False],
        #     ['14 越战越勇', 'TOPC1451467829851129', 'A5DY1h2trsLm0RMGVjVY160206', '精彩片段', 0, False],
        #     ['15 回声嘹亮', 'TOPC1451535575561597', '', '精彩看点', 14, False],
        #     ['16 幸福账单', 'TOPC1451535575561597', 'd6wx82jRexn0Qx8hoLFU160126', '精彩看点', 0, False],
        #     ['17 黄金100秒', 'http://tv.cctv.com/lm/hj100m/videoset/', '', 'WHOLE PAGE', 1, False],
        #     ['18 非常6+1', 'TOPC1451467940101208', '', '精彩看点', 14, False],
        #     ['19 综艺盛典', 'http://tv.cctv.com/lm/zysd/videoset/', '', 'WHOLE PAGE', 1, False],
        #     # ['20 天天把歌唱', '', '', 'ENTIRE SHOWS', False],
        #     ['21 星光大道超级版', 'http://tv.cctv.com/lm/xgddcjb/video/index.shtml', '', 'WHOLE PAGE', 1, False],
        #     ['22 有朋远方来', 'http://tv.cctv.com/lm/ypyfl/videoset/', '', 'WHOLE PAGE', 1, False],
        #     ['23 中国正在听', 'http://tv.cctv.com/lm/zgzzt/videoset/', '', 'WHOLE PAGE', 1, True],
        #     ['24 完美星开幕', 'http://tv.cctv.com/lm/wmxkm/videoset/', '', 'WHOLE PAGE', 1, True],
        #     ['25 巅峰音乐汇', 'http://tv.cctv.com/lm/dfyyh/videoset/', '', 'WHOLE PAGE', 2, True],
        #     ['26 “中国梦”主题歌曲展播', 'http://ent.cntv.cn/special/zgmgqz/', '', 'WHOLE PAGE', 3, False],
        #     ['27 中国民歌大会第二季', 'http://tv.cctv.com/cctv3/special/2017mgdh/bhy/', '', '视频回顾', 4, False],
        #     ['28 我和我的祖国2017', 'http://music.cctv.com/special/whwdzg2017/index.shtml', '', 'WHOLE PAGE', 5, False],
        #     ['29 2017年中秋晚会', 'http://tv.cctv.com/2017/09/21/VIDAuTggsVYiMmLnOgLnPKDB170921.shtml', '', '精彩看点', 6, True],
        #     ['30 中秋特别节目', 'http://tv.cctv.com/cctv3/special/2017wjymy/index.shtml', '', 'WHOLE PAGE', 1, True],
        #     ['31 江山如画-2017国庆音乐会', 'http://music.cctv.com/special/2017jsrh/index.shtml', '', '精彩视频', 7, True],
        #     ['32 中国梦 祖国颂2017', 'http://tv.cctv.com/2017/09/26/VIDAGMO9c7wSn9PNgP88nv8F170926.shtml', '', '精彩看点', 6,
        #      True],
        #     ['33 强军战旗红——建军90周年“心连心”赴南昌慰问演出', 'http://tv.cctv.com/2017/07/31/VIDAyJUXRTNc4saRFK5YLKvk170731.shtml', '',
        #      '精彩看点', 6, True],
        #     ['34 在党的旗帜下', 'http://tv.cctv.com/2017/08/01/VIDA9KMlXxaLT4axj4rOHwVO170801.shtml', '', '精彩看点', 6, True],
        #     ['35 守望相助草原情', 'http://tv.cctv.com/2017/08/08/VIDA2ZoXCZt81FsrgXB1yi1y170808.shtml', '', '精彩看点', 6, True],
        #     ['36 歌声飘过90年', 'http://ent.cctv.com/special/90/01/index.shtml', '', 'WHOLE PAGE', 8, True],
        #     ['37 唱支山歌给党听', 'http://music.cctv.com/special/2017czsggdt/', '', 'WHOLE PAGE', 5, True],
        #     ['38 山水寄美端午情', 'http://ent.cctv.com/special/dw/index.shtml', '', 'WHOLE PAGE', 1, True],
        #     ['39 中国梦·劳动美2017', 'http://ent.cctv.com/special/xlx/index.shtml', '', 'WHOLE PAGE', 5, True],
        #     ['40 2017春晚', 'http://chunwan.cctv.com/', '', 'WHOLE PAGE', 9, True],
        #     ['41 美丽中国唱起来', 'http://tv.cctv.com/2017/01/19/VIDALucOxtJEnqZCSSJtV9WP170119.shtml', '', '精彩看点', 6, True],
        #     ['42 启航2017', 'http://music.cctv.com/special/qihang2017/index.shtml', '', 'WHOLE PAGE', 7, True],
        #     ['43 我和我的祖国2016', 'http://music.cctv.com/special/2016gq/index.shtml', '', 'WHOLE PAGE', 7, True],
        #     ['44 中国梦 祖国颂2016', 'http://tv.cctv.com/cctv3/2016gqwh/db/index.shtml', '', 'WHOLE PAGE', 1, True],
        #     ['45 中国民歌大会第一季', 'http://tv.cctv.com/cctv3/zgmgdh/index.shtml', '', '视频回顾', 10, True],
        #     # ['46 寻找刘三姐第三季', '', '', 'ENTIRE SHOWS', True],
        #     ['47 心连心艺术团慰问演出', 'C19548', '', '精彩片段', 13, False],
        #     ['48 伟大的旗帜', 'http://tv.cctv.com/cctv3/wddqz/index.shtml', '', 'WHOLE PAGE', 1, True],
        #     ['49 中国梦·劳动美2016', 'http://tv.cctv.com/cctv3/51wh/index.shtml', '', 'WHOLE PAGE', 1, True],
        #     ['50 2016春晚', 'http://chunwan.cntv.cn/2016/index.shtml', '', 'WHOLE PAGE', 11, True],
        #     ['51 启航2016', 'VSET100257115724', '', 'WHOLE PAGE', 15, True],
        #     ['52 2015春晚', 'http://chunwan.cntv.cn/2015/', '', 'WHOLE PAGE', 1, True],
        #     # ['53 胜利与和平', 'http://ent.cntv.cn/special/slyhp/', '', 'WHOLE PAGE', 12, True],
        #     ['54 中国好歌曲第三季', 'TOPC1451984949453678', 'uRiql41hi1BNW0BX3xfB160128', '精彩片段', 0, True],
        #     ['55 中国好歌曲第二季', 'http://tv.cctv.com/lm/zghgq2/videoset/', '', 'WHOLE PAGE', 1, True],
        #     ['56 中国好歌曲', 'VSET100181076033', '', '精彩片段', 13, True],
        # ]

    def open_global_log(self):
        # Create global log
        self.global_log = logging.getLogger(self.batches_path)
        file_handler = logging.FileHandler(self.batches_path + 'global.log', mode='w')
        self.global_log.setLevel(logging.WARNING)
        self.global_log.addHandler(file_handler)

    def open_batch_log(self):
        # Create batch log
        self.current_batch_log = logging.getLogger(self.current_batch_path)
        file_handler = logging.FileHandler(self.current_batch_path + 'batch_log.log', mode='w')
        self.current_batch_log.setLevel(logging.WARNING)
        self.current_batch_log.addHandler(file_handler)

    def create_batch(self):
        while True:
            self.date = time.strftime('%Y%m%d')
            if self.date != self.date_previous_batch:
                self.current_batch_number = 1
            else:
                self.current_batch_number += 1
            self.date_previous_batch = self.date
            batch_number_4d = str(self.current_batch_number).zfill(4)
            self.current_batch_name = self.date + '_' + batch_number_4d
            self.current_batch_path = self.batches_path + self.current_batch_name + '/'
            self.tracks_path = self.current_batch_path + 'tracks/'
            if not os.path.exists(self.current_batch_path):
                os.makedirs(self.current_batch_path)
                if not os.path.exists(self.tracks_path):
                    os.makedirs(self.tracks_path)
                self.current_batch_size = 0
                self.metadata.initialize(self.current_batch_path)
                self.open_batch_log()
                break

    def delivery_complete(self):
        filename = self.current_batch_path + 'delivery.complete'
        open(filename, 'w').close()

    def get_tracks_crawled(self):
        shows_path = self.batches_path + 'shows/'
        for show in self.shows:
            file_path = shows_path + show[0] + '/tracks_to_download.xls'
            show_tracks_crawled = []
            if os.path.exists(file_path):
                xls = xlrd.open_workbook(file_path, formatting_info=True)
                n_rows = xls.sheet_by_index(0).nrows
                sheet_read = xls.sheet_by_index(0)
                for row in range(1, n_rows):
                    title = sheet_read.cell(row, 0).value
                    artist = sheet_read.cell(row, 1).value
                    url = sheet_read.cell(row, 2).value
                    dl_idx = sheet_read.cell(row, 3).value
                    show_tracks_crawled.append({
                        'title': title,
                        'artist': artist,
                        'url': url,
                        'index': dl_idx,
                    })
            show_tracks_crawled = sorted(show_tracks_crawled, key=lambda show_tracks_crawled: show_tracks_crawled['index'])
            last_tracks = []
            checkfile_path = shows_path + show[0] + '/last_tracks.xls'
            if os.path.exists(checkfile_path):
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
            show_tracks = []
            for track in show_tracks_crawled:
                if len(last_tracks) > 0:
                    all_same = False
                    if track['title'] == last_tracks[0]['title'] \
                            and track['artist'] == last_tracks[0]['artist'] \
                            and track['url'] == last_tracks[0]['url']:
                        idx = show_tracks_crawled.index(track)
                        all_same = True
                        i_max = 5
                        if len(last_tracks) < 5:
                            i_max = len(last_tracks)
                        for i in range(1, i_max):
                            if show_tracks_crawled[idx + i]['title'] == last_tracks[i]['title'] \
                                    and show_tracks_crawled[idx + i]['artist'] == last_tracks[i]['artist'] \
                                    and show_tracks_crawled[idx + i]['url'] == last_tracks[i]['url']:
                                pass
                            else:
                                all_same = False
                                break
                    if all_same:
                        break
                show_tracks.append(track)
            self.tracks_dl_list.append(show_tracks)

    def remove_batch_garbage(self):
        for file in os.listdir(self.tracks_path):
            if file.endswith('.mp4'):
                os.remove(self.tracks_path + file)

    def make_batches(self):
        self.get_tracks_crawled()
        self.remove_batch_garbage()
        print('Obtaining batches...')
        for show_tracks in self.tracks_dl_list:
            show_name = self.shows[self.tracks_dl_list.index(show_tracks)][0]
            show_path = self.batches_path + 'shows/' + show_name
            for track in show_tracks:
                track_info = track['title'] + ' - ' + track['artist']
                self.yt_downloader.download(track['url'], self.tracks_path, self.current_batch_log, track_info)

                formatted_track = Track(track['artist'], track['title'], show_name, track['url'])
                self.metadata.add_track(formatted_track, self.yt_downloader.file_url)
                self.metadata.add_to_sheet()

                self.current_batch_size += 1

                if self.current_batch_size == self.n_tracks_per_batch or \
                        (self.tracks_dl_list.index(show_tracks) == len(self.tracks_dl_list) - 1 and
                         show_tracks.index(track) == len(show_tracks) - 1):
                    print('Batch completed.')
                    self.delivery_complete()
                    self.remove_batch_garbage()
                    if not (self.tracks_dl_list.index(show_tracks) == len(self.tracks_dl_list) - 1 and
                            show_tracks.index(track) == len(show_tracks) - 1):
                        self.create_batch()
            if os.path.exists(show_path + '/last_tracks.xls'):
                os.remove(show_path + '/last_tracks.xls')
            if os.path.exists(show_path + '/tracks_to_download.xls'):
                os.remove(show_path + '/tracks_to_download.xls')
            if os.path.exists(show_path + '/last_tracks_candidates.xls'):
                os.rename(show_path + '/last_tracks_candidates.xls', show_path + '/last_tracks.xls')
