# coding: utf-8

"""
HIMYM TV Scripts Crawler.

Crawl HIMYM TV scripts from
http://transcripts.foreverdreaming.org/viewforum.php?f=177
"""

import os
from http_utils import crawl_html, openf

BASE_URL = 'http://transcripts.foreverdreaming.org'
SCRIPT_DIR = 'data/tv/himym'


def get_all_links(page_num):
    """
    Get all links from
    http://transcripts.foreverdreaming.org/viewforum.php?f=177
    """
    all_links = []
    start_url = BASE_URL + '/viewforum.php?f=177&start='

    for i in range(page_num):
        html = crawl_html(start_url + str(i * 25))
        tds = html.find_all('td', class_='topic-titles')
        for td in tds:
            href = td.find('a')['href'].split('&')[:2]
            all_links.append('&'.join(href))
    return all_links


def crawl_content(link):
    """
    Get the script content from a single page,
    http://transcripts.foreverdreaming.org/viewtopic.php?f=177&t=11508
    """
    html = crawl_html(BASE_URL + link[1:]).find('div', id='pagecontent')
    page_head = html.find('div', class_='boxheading').find('h2').text
    page_content = html.find('div', class_='postbody')
    p_list = page_content.find_all('p')
    all_ps = '\n'.join([p.text for p in p_list])
    return all_ps, page_head


def crawl_himym():
    all_links = get_all_links(9)  # 9 pages for HIMYM TV series
    print('Total links:', len(all_links))

    if not os.path.exists(SCRIPT_DIR):
        os.makedirs(SCRIPT_DIR)

    for link in all_links:
        all_ps, page_head = crawl_content(link)
        with openf(os.path.join(SCRIPT_DIR, page_head + '.txt'), 'w') as f:
            f.write(all_ps + '\n')
        print('Finished: ' + page_head)
