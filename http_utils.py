# coding: utf-8

import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/66.0.3359.139 Safari/537.36"
}


def openf(filename, mode='r', encoding='utf-8'):
    return open(filename, mode=mode, encoding=encoding, errors='ignore')


def crawl_html(url, method='GET', data=None, params=None, timeout=5, return_format='soup', headers=headers):
    try:
        if method == 'GET':  # GET
            resp = requests.get(url, params=params, headers=headers, timeout=timeout)
        else:  # POST
            resp = requests.post(url, headers=headers, data=data, timeout=timeout)

        if return_format == 'soup':  # BeautifulSoup
            return BeautifulSoup(resp.content, 'lxml')
        elif return_format == 'json':  # JSON
            return resp.json()
        elif return_format == 'text':  # 原始数据
            return resp.text
    except Exception as e:
        print(e)
        return None
