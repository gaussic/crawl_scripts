#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
歌词抓取：抓取百度音乐歌词
作者: Gaussic
"""

import requests
from bs4 import BeautifulSoup
import os

music_base_url = 'http://music.baidu.com/search/lrc'

def crawl_html_doc(params=None):
    """获取网页内容，转化为soup"""
    r = requests.get(music_base_url, params=params)
    r_content = str(r.content, encoding='utf-8', errors='ignore')
    soup = BeautifulSoup(r_content, 'html5lib')
    return soup

def fetch_page_number(singer):
    """获取总页数，一页默认20条"""
    params = {'key': singer}
    content = crawl_html_doc(params)
    return int(content.select('a.page-navigator-number')[-1].text)

def crawl_lyrics(singer):
    """逐页抓取歌词"""
    page_num = fetch_page_number(singer)
    lyric_list = []
    for i in range(page_num):
        params = {'key': singer, 'start': i * 20}
        content_list = crawl_html_doc(params)
        content_list = content_list.select('li.bb')
        for content in content_list:
            try:
                song_title = content.find('span', class_='song-title')
                song_title = song_title.find('a').get_text().strip()
                song_author = content.find('span', class_='author_list')
                song_author = song_author['title'].strip()
                song_lyric = content.find('div', class_='lrc-content')
                song_lyric = song_lyric.find('p').get_text().strip()
                lyric_list.append({'title': song_title,
                                   'author': song_author,
                                   'lyric': song_lyric})
            except:
                pass
    return lyric_list

def write_file(singer, lyric_list):
    """存为文本"""
    if not os.path.exists(singer):
        os.mkdir(singer)
    for i, content in enumerate(lyric_list):
        try:
            filename = '{0:0>3}'.format(i) + ' - ' + content['title'] + ' - ' \
                + content['author'] + '.txt'
            filename = filename.replace('/', '-')
            filename = os.path.join(singer, filename)
            open(filename, 'w', encoding='utf-8').write(content['lyric'])
        except:
            pass

if __name__ == '__main__':
    singer = '邓丽君'
    lyric_list = crawl_lyrics(singer)
    print(len(lyric_list))
    write_file(singer, lyric_list)
