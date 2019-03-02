# -*- coding: utf-8 -*-
"""Crawl info from wiki."""

import re

import requests
from bs4 import BeautifulSoup


class Wiki:

    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                    AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/71.0.3578.98 Safari/537.36',
        }
        self.link = 'https://en.wikipedia.org/wiki'
        self.param_dicts = {}

    def get_response(self, keyword):
        url = '{}/{}'.format(self.link, keyword)

        try:
            response = requests.get(url,
                                    headers=self.headers,
                                    params=self.param_dicts,
                                    timeout=9)
            if response.raise_for_status() is None:
                response.encoding = response.apparent_encoding
                return response
        except requests.exceptions.RequestException:
            return

    def parse_response(self, response):
        try:
            soup = BeautifulSoup(response.text, 'lxml')
            body_content = soup.find('div', id='bodyContent')
            text = body_content.get_text(' ', strip=True)
            if text:
                clear_txt = re.findall(r"[\u4E00-\u9FA5A-Za-z ]", text)
                txt = ''.join(clear_txt)
            return txt
        except Exception:
            return


# test
if __name__ == '__main__':
    import time
    # with ProcessPoolExecutor(crawler.maxprocesses) as executor:
    #     pr_fs = executor.map([crawler.do_ch(), crawler.do_eg()])

    bt = time.time()
    w = Wiki()
    res = w.get_response('English')
    mark = time.time()
    print(mark - bt)
    text = w.parse_response(res)
    print(len(text))
    print(time.time() - mark)

    # import os
    # d = os.path.dirname(os.path.abspath(__file__))
    # t_path = os.path.join(d, 'test.txt')
    # with open(t_path, 'w') as f:
    #     f.write(text)
