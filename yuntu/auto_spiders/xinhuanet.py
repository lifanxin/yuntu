# -*- coding: utf-8 -*-
"""Crawl info from xinhuanet."""

import requests
from bs4 import BeautifulSoup


class Xinhuanet:

    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                    AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/71.0.3578.98 Safari/537.36',
        }
        self.link = 'http://so.news.cn/getNews?'
        # low search
        # self.param_dicts = {
        #     'keyword': None,
        #     'curPage': 1,
        #     'sortField': 0,
        #     'searchFields': 1,
        #     'lang': 'cn'
        # }

        # high search
        self.param_dicts = {
            'keyWordAll': None,
            'keyWordOne': None,
            'keyWordIg': None,
            'searchFields': 1,
            'sortField': 0,
            'url': 'www.xinhuanet.com',
            'senSearch': 1,
            'lang': 'cn',
            'keyword': None,
            'curPage': 1
        }

    # just get one page for the latest
    def get_news(self, keyword):
        self.param_dicts['keyword'] = keyword
        self.param_dicts['keyWordAll'] = keyword
        print('Xinhuanet spider get start...\n'
              'catch keyword: {}'.format(keyword))

        try:
            res = requests.get(self.link,
                               headers=self.headers,
                               params=self.param_dicts,
                               timeout=9)
            if res.raise_for_status() is None:
                res.encoding = res.apparent_encoding
                for info in res.json()['content']['results']:
                    try:
                        yield \
                            info.get('title').replace('<font color=red>', '') \
                                .replace('</font>', ''), \
                            info.get('url'), \
                            info.get('pubtime')
                    except Exception:
                        continue
        except Exception:
            return

    def get_response(self, article_data):
        url = article_data[1]

        try:
            response = requests.get(url,
                                    headers=self.headers,
                                    timeout=9)
            if response.raise_for_status() is None:
                response.coding = response.apparent_encoding
                return response
        except Exception:
            return

    def parse_response(self, response):
        try:
            response.encoding = response.apparent_encoding
            soup = BeautifulSoup(response.text, 'lxml')
            article_content = soup.find('div', class_='p-right left')
            if not article_content:
                # got two type html
                article_content = soup.find('div', class_='content pack')
            text = article_content.get_text(' ', strip=True)
            return text
        except Exception:
            return


# test
if __name__ == '__main__':
    x = Xinhuanet()
    iters = x.get_news('百度')
    # test = next(iters)
    # print(test)
    # res = x.get_response(test)
    # text = x.parse_response(res)
    # print(text)
    for article_data in iters:
        print('yes: {}'.format(article_data[1]))
        res = x.get_response(article_data)
        text = x.parse_response(res)
        if not text:
            print('None: {}'.format(article_data[1]))
        # print(len(text))
        print(text)

    # import os
    # d = os.path.dirname(os.path.abspath(__file__))
    # t_path = os.path.join(d, 'test.txt')
    # with open(t_path, 'w') as f:
    #     f.write(text)
