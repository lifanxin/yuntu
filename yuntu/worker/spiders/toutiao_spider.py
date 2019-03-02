# -*- coding : utf-8 -*-
"""Crawl toutiao's news.

python: 3.6.7
Copyright 2019-01-26 @lifanxin
"""
import requests
from bs4 import BeautifulSoup
import re
import jieba


class NewsSpider:
    """Crawl news spider."""
    # https://www.toutiao.com/api/search/content/?aid=24&app_name=web_search&offset=0&format=json&keyword=百度&autoload=true&count=20&en_qc=1&cur_tab=1&from=search_tab&pd=synthesis
    # https://www.toutiao.com/api/search/content/?aid=24&app_name=web_search&offset=0&format=json&keyword=上海冰鉴&autoload=true&count=20&en_qc=1&cur_tab=1&from=search_tab&pd=synthesis
    toutiao_news = 'https://www.toutiao.com/api/search/content/?'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                    AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/71.0.3578.98 Safari/537.36',
    }
    param_dicts = {
        'aid': 24,
        'offset': 0,
        'format': 'json',
        'keyword': None,
        'autoload': 'true',
        'count': 20,
        'cur_tab': 1,
        'from': 'search_tab',
        'pd': 'synthesis'
    }

    def __init__(self, keyword):
        """Init the spider.

        :param keyword: what you want to ask.
        """
        NewsSpider.param_dicts['keyword'] = keyword

    def get_news(self):
        """Get news's info first.

        title: news's title.
        group_id: make up url for news's content.
        datetime: the news's publish time.
        """
        r = requests.get(NewsSpider.toutiao_news,
                         headers=NewsSpider.headers,
                         params=NewsSpider.param_dicts)
        if r.status_code == 200:
            for info in r.json()['data']:
                try:
                    yield info['title'], info['group_id'], info['datetime']
                except KeyError:
                    continue

    def get_content(self, group_id):
        """Get news content."""
        url = 'https://www.toutiao.com/{}{}/'.format('a', group_id)
        r = requests.get(url, headers=NewsSpider.headers)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'lxml')
            string = soup.find_all("script")[6].text
            pattern = re.compile(r"content: (.*)(\s*)groupId")
            info = re.search(pattern, string)
            # print(info.groups()[0])
            seg_list = jieba.cut(info.groups()[0], cut_all=False)
            for i in seg_list:
                print(i)


if __name__ == '__main__':
    n = NewsSpider('冰鉴科技')
    iter = n.get_news()
    n.get_content(next(iter, None)[1])
