# -*- coding: utf-8 -*-
"""Crawl info from toutiao."""

import re

import requests
from bs4 import BeautifulSoup


class Toutiao:

    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                    AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/71.0.3578.98 Safari/537.36',
        }
        self.link = 'https://www.toutiao.com/api/search/content/?'
        self.param_dicts = {
            'aid': 24,
            'app_name': 'web_search',
            'offset': 0,
            'format': 'json',
            'keyword': None,
            'autoload': 'true',
            'count': 20,
            'en_qc': 1,
            'cur_tab': 1,
            'from': 'search_tab',
            'pd': 'synthesis'
        }

    # just get one page for the latest
    def get_news(self, keyword):
        self.param_dicts['keyword'] = keyword
        print('Toutiao spider get start...\ncatch keyword: {}'.format(keyword))

        try:
            res = requests.get(self.link,
                               headers=self.headers,
                               params=self.param_dicts,
                               timeout=9)
            if res.raise_for_status() is None:
                res.encoding = res.apparent_encoding
                for info in res.json()['data']:
                    try:
                        yield info.get('title'), \
                            info.get('group_id'), \
                            info.get('datetime')
                    except Exception:
                        continue
        except Exception:
            return

    def get_response(self, article_data):
        group_id = article_data[1]
        url = 'https://www.toutiao.com/{}{}/'.format('a', group_id)
        # print('get content form url: {}'.format(url))

        try:
            response = requests.get(url,
                                    headers=self.headers,
                                    params={},
                                    timeout=9)
            if response.raise_for_status() is None:
                response.encoding = response.apparent_encoding
                return response
        except Exception:
            return

    def parse_response(self, response):
        try:
            soup = BeautifulSoup(response.text, 'lxml')
            text = soup.find_all("script")[6].get_text()
            # accurate match article
            # pattern = re.compile(r"content: (.*)(\s*)groupId")
            # info = re.search(pattern, text).groups()[0]
            if text:
                # keep space, may be useful for cut
                clear_txt = re.findall(r"[\u4E00-\u9FA5 ]", text)
                txt = ''.join(clear_txt)
            return txt
        except Exception:
            return


# test
if __name__ == '__main__':
    import time

    bt = time.time()
    t = Toutiao()
    iters = t.get_news('百度')
    for article_data in iters:
        print(article_data)
        res = t.get_response(article_data)
        text = t.parse_response(res)
        # print(len(text))
        print(text)
    et = time.time()
    print('all time: {}'.format(et - bt))

    # import os
    # d = os.path.dirname(os.path.abspath(__file__))
    # t_path = os.path.join(d, 'test.txt')
    # with open(t_path, 'w') as f:
    #     f.write(text)
