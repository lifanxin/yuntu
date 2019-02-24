# -*- coding: utf-8 -*-
"""Crawl info from baike."""

import requests
from bs4 import BeautifulSoup


class Baidu:

    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                    AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/71.0.3578.98 Safari/537.36',
        }
        self.link = 'https://baike.baidu.com/item'
        self.param_dicts = {}

    def get_response(self, keyword):
        url = '{}/{}'.format(self.link, keyword)

        try:
            response = requests.get(url,
                                    headers=self.headers,
                                    params=self.param_dicts,
                                    timeout=10)
            if response.raise_for_status() is None:
                response.encoding = response.apparent_encoding
                return response
        except requests.exceptions.RequestException:
            return

    def parse_response(self, response):
        try:
            soup = BeautifulSoup(response.text, 'lxml',
                                 from_encoding=response.encoding)
            main_content = soup.find('div', class_='main-content')
            return main_content.get_text(' ', strip=True)
        except Exception:
            return


# test
if __name__ == '__main__':
    b = Baidu()
    res = b.get_response('马云')
    text = b.parse_response(res)
    print(len(text))

    import os
    d = os.path.dirname(os.path.abspath(__file__))
    t_path = os.path.join(d, 'test.txt')
    with open(t_path, 'w') as f:
        f.write(text)
