# coding: utf-8


from ts_crawler.himym_crawl import crawl_himym
from ts_crawler.tbbt_crawl import crawl_tbbt
from ts_crawler.imsdb_crawler import crawl_imsdb
from lyric_crawler.baidu_lyric_crawler import crawl_lyrics
from lyric_crawler.netease_lyric_crawler import find_artist_ids, crawl_all_artists

if __name__ == '__main__':
    # crawl_himym()
    # crawl_tbbt()
    # crawl_imsdb()
    crawl_lyrics('邓丽君')
    # find_artist_ids()
    # crawl_all_artists()
