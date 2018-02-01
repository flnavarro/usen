# -*- coding: utf-8 -*-

# Scrapy settings for netherlands_radio project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

USER_AGENT = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'

BOT_NAME = 'CCTV'
SPIDER_MODULES = ['CCTV.spiders']
NEWSPIDER_MODULE = 'CCTV.spiders'