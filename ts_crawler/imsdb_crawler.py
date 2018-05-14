# coding: utf-8

"""
IMSDb Movie crawler.

Crawl IMSDb movie scripts from http://www.imsdb.com/
"""

import os
from urllib.parse import quote
from http_utils import crawl_html, openf

BASE_URL = 'http://www.imsdb.com'
SCRIPT_DIR = 'data/movie/imsdb'


def clean_script(text):
    text = text.replace('Back to IMSDb', '')
    text = text.replace('''<b><!--
</b>if (window!= top)
top.location.href=location.href
<b>// -->
</b>
''', '')
    text = text.replace('''          Scanned by http://freemoviescripts.com
          Formatting by http://simplyscripts.home.att.net
''', '')
    return text.replace(r'\r', '')


def get_script(relative_link):
    tail = relative_link.split('/')[-1]
    print('Fetching %s' % tail)
    script_front_url = BASE_URL + quote(relative_link)

    try:
        front_html = crawl_html(script_front_url)
        script_link = front_html.find('p', align="center").a['href']
    except:
        print('%s has no script :(' % tail)
        return None, None

    if script_link.endswith('.html'):
        title = script_link.split('/')[-1].split(' Script')[0]
        script_html = crawl_html(BASE_URL + script_link)
        script_text = script_html.find('td', {'class': "scrtext"}).get_text()
        script_text = clean_script(script_text)
        return title, script_text
    else:
        print('%s is a pdf :(' % tail)
        return None, None


def crawl_imsdb():
    start_url = 'http://www.imsdb.com/all%20scripts/'
    paragraphs = crawl_html(start_url).find_all('p')

    if not os.path.exists(SCRIPT_DIR):
        os.makedirs(SCRIPT_DIR)

    for p in paragraphs:
        relative_link = p.a['href']
        title, script = get_script(relative_link)
        if not script:
            continue
        cur_filename = os.path.join(SCRIPT_DIR, title.strip('.html') + '.txt')
        with openf(cur_filename, 'w') as f:
            f.write(script)
