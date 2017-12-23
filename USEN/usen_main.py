# -*- coding: utf-8 -*-
from scrapy.crawler import CrawlerProcess
from USEN import settings
from spiders.usen_spider import UsenSpider
from metadata_formatter import format_metadata


class UsenCrawler(object):

    def __init__(self):
        self.spider = UsenSpider
        self.process = None

    def get_current_tracks(self):
        self.process = CrawlerProcess({
            'USER AGENT': settings.USER_AGENT,
            'SPLASH_URL': settings.SPLASH_URL,
            'DOWNLOADER_MIDDLEWARES': settings.DOWNLOADER_MIDDLEWARES,
            'SPIDER_MIDDLEWARES': settings.SPIDER_MIDDLEWARES,
            'DUPEFILTER_CLASS': settings.DUPEFILTER_CLASS,
            'HTTPCACHE_STORAGE': settings.HTTPCACHE_STORAGE
        })
        self.process.crawl(self.spider)
        self.process.start()


usen_crawler = UsenCrawler()

usen_crawler.get_current_tracks()

# TODO: Implement timer to be updating data each X seconds/minutes

# metadata_examples = [
#     'あなたといきてゆく ／ ＧＬＡＹ',
#     # OK
#     'ハウ・ドゥ・アイ・リヴ ／ スタジオＵＳＥＮ', # A-10, A-11, A-14, A-15
#     # OK
#
#     '＜モーツァルト／エドヴァルド・グリーグ＞ ピアノ・ソナタ　第１５番　ハ長調　Ｋ．５４５（４手ピアノ編曲版）　第２楽章 ／ ｐ）マルタ・アルゲリッチ、ピョートル・アンデルジェフスキー',
#     # ??
#     'ダイサナジャー ／ 上原長幸／大城みどり／玉城美智子',
#     '豊年の歌 ／ 宮国米男／砂川きよみ',
#     # OK?
#     'ワン・オブ・アス（『ブルース・オールマイティ』より） ／ ジョーン・オズボーン',
#     # OK
#     'レッツ・ゲット・イット・オン （Ｓｉｎｇｌｅ　Ｅｄｉｔ） ／ マーヴィン・ゲイ',
#     # OK?
#
#     '(26位) １００ｄｅｇｒｅｅｓ ／ ＴＨＥ　ＲＡＭＰＡＧＥ　ｆｒｏｍ　ＥＸＩＬＥ　ＴＲＩＢＥ',
#     # OK
#     '(注目曲) すてきなホリデイ ／ ＳＨＯＷＳＴＯＰＰＥＲＳ',
#     # OK
#     '(17) Ｎｅｗ　Ｒｕｌｅｓ ／ Ｄｕａ　Ｌｉｐａ',
#     # OK
#     '(Recommend) Ｌｅｔ　Ｙｏｕ　Ｄｏｗｎ ／ ＮＦ',
#     # OK
#     'Ｕｐ　Ｏｎ　Ｔｈｅ　Ｈｏｕｓｅｔｏｐ ／ Ｂｅｅｇｉｅ　Ａｄａｉｒ／Ｊａｃｋ　Ｊｅｚｚｒｏ／Ｄｅｎｉｓ　Ｓｏｌｅｅ／Ｓａｍ　Ｌｅｖｉｎｅ／Ｇｅｏｒｇｅ　Ｔｉｄｗｅｌｌ／Ｒｏｇｅｒ　Ｓｐｅｎｃｅｒ／Ｃｈｒｉｓ　Ｂｒｏｗｎ',
#     # OK
#     'Ｉｎｆｏ ／ ＊＊＊',  # C43
#     # OK
#
#     '『０』 ／ Ｈａｌｆ　ｔｉｍｅ　Ｏｌｄ',
#     # OK
#     '【ありがとう】これからも ／ カイワレハンマー',
#     # OK
#     '(10位) Ｒｅａｓｏｎ！！【アニメ　アイドルマスター　ＳｉｄｅＭ】 ／ ３１５　ＳＴＡＲＳ（ＤＲＡＭＡＴＩＣ　ＳＴＡＲＳ、Ｂｅｉｔ、Ｓ．Ｅ．Ｍ、Ｈｉｇｈ×Ｊｏｋｅｒ、Ｗ、Ｊｕｐｉｔｅｒ）',
#     # OK
#
#     '＜ベートーヴェン＞ 交響曲　第９番　ニ短調　Ｏｐ．１２５　「合唱」　第１楽章 ／ 指揮）ハンス・シュミット＝イッセルシュテット　Ｓ）ジョーン・サザーランド＆Ｍｓ）マリリン・ホーン＆Ｔ）ジェイムズ・キング＆Ｂｓ）マルッティ・タルヴェラ＆ウィーン・フィルハーモニー管弦楽団＆ウィーン国立歌劇場合唱団',
#     # OK ?
#     '＜Ｊ．Ｓ．バッハ＞ 無伴奏チェロ組曲　第３番　ハ長調　ＢＷＶ．１００９　クーラント ／ ｖｃ）アンナー・ビルスマ',
#     # OK ?
#     '【Ｒａｖｅｌ】Ｐａｖａｎｅ　Ｐｏｕｒ　Ｕｎｅ　Ｉｎｆａｎｔｅ　Ｄｅｆｕｎｔｅ ／ Ｐａｕｌ　Ｃｒｏｓｓｌｅｙ', # B-38
#     # OK ?
#
#     'a-FAN FAN１９【水樹奈々POWER GATE第１８９回】～トーク ／ （ＤＪ）水樹奈々', # C-26
#     '【内田真礼の「真礼充ラジオ」第１２１回】～トーク ／ （ＤＪ）内田真礼', # C-26
#     '【ファイティングミュージック・リターンズ】～トーク ／ (DJ)山川豊　岩佐美咲', # C-42
#     '【Ｖｉｎｔａｇｅ　Ｍｕｓｉｃ】～トーク ／ （ＤＪ）レイチェル・チャン', #C43
#     '【舞台やろうっ！　黒羽麻璃央の音言】～トーク ／ （ＤＪ）黒羽麻璃央',  # C43,
#
#     'Ｒｅｄ　Ｂａｔｔｌｅ 【アニメ　この素晴らしい世界に祝福を！２】 ／ めぐみん（ＣＶ：高橋李依）、ゆんゆん（ＣＶ：豊崎愛生）', #C54
#     # ok?
# ]
#
# title, artist = format_metadata(metadata_examples[24])
#
# print(title, artist)

# METADATA
# * title / artist
#   A
#   * DUDAS FORMATO: A-08, A-12
#   * NADA en
#       A-> 16
#       B->
#       C-> 29-36, 68-70
#       D->
#       E-> 16-19
#       F
#       G-> 36,40




