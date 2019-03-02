# -*- coding: utf-8 -*-
"""Crawl info from people."""

import requests
from bs4 import BeautifulSoup


class People:

    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                    AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/71.0.3578.98 Safari/537.36',
        }
        self.link = 'http://search.people.com.cn/cnpeople/search.do?'
        self.param_dicts = {
            'pageNum': 1,
            'keyword': None,
            'siteName': 'news',
            'facetFlag': 'true',
            'nodeType': 'belongsId',
            'nodeId': 0
        }

    # just get one page for the latest
    def get_news(self, keyword):
        self.param_dicts['keyword'] = keyword.encode('gbk')
        print('People spider get start...\ncatch keyword: {}'.format(keyword))

        try:
            res = requests.post(self.link,
                                headers=self.headers,
                                data=self.param_dicts,
                                timeout=9)
            if res.raise_for_status() is None:
                res.encoding = res.apparent_encoding
                soup = BeautifulSoup(res.text, 'lxml')
                fr_w = soup.find('div', class_='fr w800')
                for ul in fr_w.find_all('ul'):
                    try:
                        children = ul.contents

                        title = children[0].get_text()
                        url_and_time = children[4].get_text().split(' ', 1)
                        url = url_and_time[0]
                        time = url_and_time[1].strip()

                        yield title, url, time
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
            article_content = soup.find('div', class_='box_con')
            if not article_content:
                # got two type html
                article_content = soup.find('div', class_='gray box_text')
            text = article_content.get_text(' ', strip=True)
            return text
        except Exception:
            return


# test
if __name__ == '__main__':
    p = People()
    iters = p.get_news('阿里')
    test = next(iters)
    # print(test)
    # res = p.get_response(test)
    # text = p.parse_response(res)
    # print(text)
    for article_data in iters:
        print(article_data)
        res = p.get_response(article_data)
        text = p.parse_response(res)
        if not text:
            continue
        print(len(text))
        print(text)

    # import os
    # d = os.path.dirname(os.path.abspath(__file__))
    # t_path = os.path.join(d, 'test.txt')
    # with open(t_path, 'w') as f:
    #     f.write(text)
