# coding: utf-8

"""
歌词抓取：抓取百度音乐歌词
作者: Gaussic
"""

import os
from http_utils import crawl_html, openf

BASE_URL = 'http://music.baidu.com/search/lrc'
BASE_DIR = 'data/lyric/baidu'


def crawl_lyrics(singer):
    """逐页抓取歌词"""
    html = crawl_html(BASE_URL, params={'key': singer}, timeout=10)
    page_num = int(html.select('a.page-navigator-number')[-1].text)
    print('歌手 %s 共 %d 页' % (singer, page_num))

    SINGER_DIR = os.path.join(BASE_DIR, singer)
    if not os.path.exists(SINGER_DIR):
        os.makedirs(SINGER_DIR)

    cnt = 1
    for i in range(page_num):
        params = {'key': singer, 'start': i * 20}
        content_list = crawl_html(BASE_URL, params=params, timeout=10).select('li.bb')
        for content in content_list:
            try:
                title = content.find('span', class_='song-title').find('a').text.strip()
                author = content.find('span', class_='author_list')['title'].strip()
                if singer not in author:
                    continue
                lyric = content.find('div', class_='lrc-content').find('p').text.strip()
                filename = title + ' - ' + author + ' - ' + '{0:0>4}'.format(cnt) + '.txt'
                filename = filename.replace('/', '-')
                openf(os.path.join(SINGER_DIR, filename), 'w').write(lyric)
                print(filename)
                cnt += 1
            except:
                pass
        print('完成，第 %d 页' % (i + 1))
