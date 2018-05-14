# coding: utf-8

"""
TBBT TV Scripts Crawler.

Crawl TBBT TV scripts from
http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8506
"""

import os
from http_utils import crawl_html, openf

BASE_URL = 'http://transcripts.foreverdreaming.org'
SCRIPT_DIR = 'data/tv/tbbt'


def get_all_links():
    """
    Get all links from
    http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8506
    """
    all_links = []
    link_url = BASE_URL + '/viewtopic.php?f=159&t=8506'
    html = crawl_html(link_url)
    p_list = html.find('div', class_='postbody').find_all('p')
    for p in p_list:
        if '-' in p.text:
            all_links.append(p.find('a', class_='postlink')['href'])
    return all_links


def crawl_content(link):
    """
    Get the script content from a single page,
    http://transcripts.foreverdreaming.org/viewtopic.php?f=177&t=11508
    """
    html = crawl_html(link).find('div', id='pagecontent')
    page_head = html.find('div', class_='boxheading').find('h2').text
    page_content = html.find('div', class_='postbody')
    p_list = page_content.find_all('p')
    all_ps = '\n'.join([p.text for p in p_list])
    return all_ps, page_head


def crawl_tbbt():
    all_links = get_all_links()
    print('Total links:', len(all_links))

    if not os.path.exists(SCRIPT_DIR):
        os.makedirs(SCRIPT_DIR)

    for link in all_links:
        all_ps, page_head = crawl_content(link)
        page_head = page_head.replace('/', '_')
        with openf(os.path.join(SCRIPT_DIR, page_head + '.txt'), 'w') as f:
            f.write(all_ps + '\n')
        print('Finished: ' + page_head)
