# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import youtube_dl
import os
from os.path import splitext
import logging
import xlwt
import xlrd


class MyLogger(object):
    def __init__(self, logger, url, title, artist, show_name, recover_file, batch_path, recover_mode):
        self.logger = logger
        self.title = title
        self.artist = artist
        self.url = url
        self.recover_file = recover_file
        self.recover_mode = recover_mode
        self.batch_path = batch_path
        self.show_name = show_name

    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        if 'content too short' in msg:
            # Print error into batch log
            self.logger.warning('TRACK: ' + self.title + ' - ' + self.artist + ' -> ' + msg)
            self.error_temp()
            if not self.recover_mode:
                # Save in xls
                tracks_to_recover = []
                if not os.path.exists(self.recover_file):
                    self.create_recover_download()
                else:
                    xls = xlrd.open_workbook(self.recover_file, formatting_info=True)
                    n_rows = xls.sheet_by_index(0).nrows
                    sheet_read = xls.sheet_by_index(0)
                    for row in range(1, n_rows):
                        title = sheet_read.cell(row, 0).value
                        artist = sheet_read.cell(row, 1).value
                        url = sheet_read.cell(row, 2).value
                        show = sheet_read.cell(row, 3).value
                        tracks_to_recover.append({
                            'title': title,
                            'artist': artist,
                            'url': url,
                            'show': show
                        })
                new_track = {
                    'title': self.title,
                    'artist': self.artist,
                    'url': self.url,
                    'show': self.show_name.decode('utf-8')
                }
                tracks_to_recover.append(new_track)
                xls = xlwt.Workbook()
                sheet = xls.add_sheet('Tracks to recover')
                sheet.write(0, 0, 'Track Title')
                sheet.write(0, 1, 'Track Artist')
                sheet.write(0, 2, 'Track URL')
                sheet.write(0, 3, 'Show Name')
                row = 1
                for track in tracks_to_recover:
                    sheet.write(row, 0, track['title'])
                    sheet.write(row, 1, track['artist'])
                    sheet.write(row, 2, track['url'])
                    sheet.write(row, 3, track['show'])
                    row += 1
                xls.save(self.recover_file)

    def create_recover_download(self):
        if not os.path.isfile(self.batch_path + 'recover.download'):  # if the path doesn't exist
            file_path = self.batch_path + 'recover.download'  # create file
            open(file_path, 'w').close()

    def error_temp(self):
        file_path = self.batch_path + 'error.temp'
        open(file_path, 'w').close()


class YoutubeDownloader(object):
    def __init__(self):
        self.file_url = ''
        self.tracks_path = ''
        self.batch_path = ''
        self.error_count = 0
        self.recover_file = ''

    def my_hook(self, d):
        if d['status'] == 'finished':
            root, ext = splitext(d['filename'])
            self.file_url = root[root.find('tracks'):]
            print('Done downloading, now converting... ')

    def download(self, url, title, artist, path, show_name, logger, recover_mode):
        self.tracks_path = path
        self.batch_path = self.tracks_path[:len(self.tracks_path)-len('tracks/')]
        self.recover_file = self.batch_path + 'tracks_to_recover.xls'

        ydl_opts = {
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
            'logger': MyLogger(logger, url, title, artist, show_name, self.recover_file, self.batch_path, recover_mode),
            'progress_hooks': [self.my_hook],
            'ignoreerrors': True,
            'forcetitle': True,
            'max_downloads': 5,
            'outtmpl': path + title + ' - ' + artist + '.%(ext)s',
        }

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                print('Downloading track... ' + title + ' - ' + artist)
                ydl.download([url])
        except youtube_dl.utils.DownloadError:
            print('Download Error')

    @staticmethod
    def remove_recover_download(batch_path):
        # remove file
        file_path = batch_path + 'recover.download'
        os.remove(file_path)
