# coding: utf-8

import os
from http_utils import crawl_html, openf

BASE_URL = "http://music.163.com"
START_URL = BASE_URL + "/artist/album?id={}&limit=100"  # 根据歌手的id，抓取其专辑列表
SONG_URL = BASE_URL + "/api/song/lyric?id={}&lv=1&kv=1&tv=-1"  # 根据歌曲的id，抓取歌词
BASE_DIR = 'data/lyric/netease/'
if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/66.0.3359.139 Safari/537.36",
    "Referer": "http://music.163.com",
    "Host": "music.163.com"
}


def crawl_lyrics(art_id):
    """抓取一整个歌手的所有歌词"""
    html = crawl_html(START_URL.format(art_id), headers=headers)  # 先抓该歌手的专辑列表

    artist = html.find('h2', id='artist-name').text.replace(' ', '_').strip()
    artist_dir = BASE_DIR + artist
    if not os.path.exists(artist_dir):  # 歌手目录
        os.makedirs(artist_dir)
    print("歌手名：", artist)

    albums = html.find('ul', class_='m-cvrlst').find_all('a', class_='msk')  # 专辑列表
    for album in albums:
        html = crawl_html(BASE_URL + album.get('href'), headers=headers)  # 再抓取该专辑下歌曲列表

        album_title = html.find('h2', class_='f-ff2').text.replace(' ', '_').replace('/', '_').strip()   # '/'会影响目录
        album_dir = os.path.join(artist_dir, album_title)
        if not os.path.exists(album_dir):  # 专辑目录
            os.mkdir(album_dir)
        print("  " + artist + "---" + album_title)

        links = html.find('ul', class_='f-hide').find_all('a')  # 歌曲列表
        for link in links:
            song_name = link.text.replace(' ', '_').replace('/', '_').strip()
            song_id = link.get('href').split('=')[1]
            try:
                lyric_json = crawl_html(SONG_URL.format(song_id), return_format='json', headers=headers)  # 抓取歌词
                lyric_text = lyric_json['lrc']['lyric']
                openf(os.path.join(album_dir, song_name + '.txt'), 'w').write(lyric_text)
                print("    " + song_name + ", URL: " + SONG_URL.format(song_id))
            except:
                print("    " + song_name + ": 无歌词, URL: " + SONG_URL.format(song_id))
        print()


def find_artist_ids():
    """只能拿到前100位的歌手ID"""
    url = 'http://music.163.com/api/artist/top?limit=100&offset=0'
    html = crawl_html(url, return_format='json', headers=headers)
    artists = html['artists']
    with openf(BASE_DIR + 'artists.txt', 'w') as fa:
        for artist in artists:
            artist_name = artist['name'].strip().replace(" ", "_")
            fa.write(artist_name + ' ' + str(artist['id']) + '\n')

def crawl_all_artists():
    with open(BASE_DIR + 'artists.txt', 'r', encoding='utf-8') as f:
        for line in f:
            art_id = line.strip().split()[1]
            crawl_lyrics(art_id)
