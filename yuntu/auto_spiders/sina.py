# -*- coding: utf-8 -*-
"""Crawl info from sina."""

import datetime

import requests
from bs4 import BeautifulSoup


class Sina:

    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                    AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/71.0.3578.98 Safari/537.36',
        }
        self.link = 'http://api.search.sina.com.cn/?'
        self.param_dicts = {
            'c': 'news',
            'q': None,
            'stime': None,
            'etime': None,
            'sort': 'rel',
            'highlight': '1',
            'num': '10',
            'ie': 'utf-8'
        }
        self.try_time = 5

    def get_date(self):
        etime = datetime.date.today() + datetime.timedelta(days=1)
        stime = etime - datetime.timedelta(weeks=3)
        return stime, etime

    # just get one page for the latest
    def get_news(self, keyword):
        # get news of three weeks
        stime, etime = self.get_date()
        self.param_dicts['q'] = keyword
        self.param_dicts['stime'] = stime
        self.param_dicts['etime'] = etime
        print('Sina spider get start...\ncatch keyword: {}'.format(keyword))

        # max try time: 5
        while self.try_time > 0:
            self.try_time -= 1
            try:
                res = requests.get(self.link,
                                   headers=self.headers,
                                   params=self.param_dicts,
                                   allow_redirects=False,
                                   timeout=9)
                if res.raise_for_status() is None:
                    res.encoding = res.apparent_encoding
                    lists = res.json()['result']['list']
                    for info in lists:
                        try:
                            yield info.get('origin_title'), \
                                info.get('url'), \
                                info.get('datetime')
                        except Exception:
                            continue
                    if lists:
                        break
            except Exception:
                continue

    def get_response(self, article_data):
        url = article_data[1]

        try:
            response = requests.get(url,
                                    headers=self.headers,
                                    timeout=9)
            if response.raise_for_status() is None:
                response.encoding = response.apparent_encoding
                return response
        except Exception:
            return

    def parse_response(self, response):
        try:
            soup = BeautifulSoup(response.text, 'lxml')
            article_content = soup.find('div', class_='article-content-left')
            text = article_content.get_text(' ', strip=True)
            return text
        except Exception:
            return


# test
if __name__ == '__main__':
    s = Sina()
    iters = s.get_news('百度')
    for article_data in iters:
        print(article_data)
        res = s.get_response(article_data)
        text = s.parse_response(res)
        print(text)

    # import os
    # d = os.path.dirname(os.path.abspath(__file__))
    # t_path = os.path.join(d, 'test.txt')
    # with open(t_path, 'w') as f:
    #     f.write(text)
