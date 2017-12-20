# -*- coding: utf-8 -*-
import unicodedata


def format_metadata(raw_metadata):
    separator = ' ／ '
    title = 'N/A'
    artist = 'N/A'
    if separator in raw_metadata:
        raw_track = raw_metadata.split(separator)
        title = clean_title(unicodedata.normalize('NFKC', raw_track[0].decode('utf-8')))
        artist = clean_artist(unicodedata.normalize('NFKC', raw_track[1].decode('utf-8')))
    return title, artist


def clean_title(title):
    if title[-1] == ' ':
        title = title[:-1]
    if title[0] == '(':
        title = title.split(')')[1][1:]
    if 'a-FAN FAN' in title:
        id_begin = title.find('a-FAN FAN')
        id_end = id_begin + len('a-FAN FAN') + 3
        title = title[:id_begin] + title[id_end:]
    if title == 'Info':
        title = 'N/A'
    return title


def clean_artist(artist):
    if artist[0] == ' ':
        artist = artist[1:]
    if 'USEN' in artist:
        artist = artist.replace('USEN', '')
    # if '(DJ)' in artist:
    #     artist = artist.replace('(DJ)', '')
    if artist == '***':
        artist = 'N/A'
    return artist
