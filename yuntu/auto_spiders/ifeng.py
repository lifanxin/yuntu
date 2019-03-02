# -*- coding: utf-8 -*-
"""Crawl info from ifeng."""

import re

import requests
from bs4 import BeautifulSoup


class Ifeng:

    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                    AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/71.0.3578.98 Safari/537.36',
        }
        self.link = 'https://search.ifeng.com/sofeng/search.action?'
        self.param_dicts = {
            'q': None,
            'c': 1
        }

    # just get one page for the latest
    def get_news(self, keyword):
        self.param_dicts['q'] = keyword
        print('Ifeng spider get start...\ncatch keyword: {}'.format(keyword))

        try:
            res = requests.get(self.link,
                               headers=self.headers,
                               params=self.param_dicts,
                               timeout=9)
            if res.raise_for_status() is None:
                res.encoding = res.apparent_encoding
                soup = BeautifulSoup(res.text, 'lxml')
                main_results = soup.find_all('div', class_='searchResults')
                for result in main_results:
                    try:
                        tag = result.find('a')

                        title = tag.get_text()
                        url = tag.get('href')
                        mark_and_time = result.contents[5].get_text()
                        time = mark_and_time.replace('凤凰资讯', '').strip()

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
                response.encoding = response.apparent_encoding
                return response
        except Exception:
            return

    def parse_response(self, response):
        try:
            soup = BeautifulSoup(response.text, 'lxml')
            article_content = soup.find('script', id='__INITIAL_STATE__')
            text = article_content.get_text(' ', strip=True)
            if text:
                clear_txt = re.findall(r"[\u4E00-\u9FA5 ]", text)
                txt = ''.join(clear_txt)
                return txt
        except Exception:
            return


# test
if __name__ == '__main__':
    i = Ifeng()
    iters = i.get_news('百度')
    for article_data in iters:
        print(article_data)
        res = i.get_response(article_data)
        print(len(res.text))
        text = i.parse_response(res)
        print(text)

    # import os
    # d = os.path.dirname(os.path.abspath(__file__))
    # t_path = os.path.join(d, 'test.txt')
    # with open(t_path, 'w') as f:
    #     f.write(text)
