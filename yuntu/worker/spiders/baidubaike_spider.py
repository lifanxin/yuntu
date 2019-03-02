# -*- coding: utf-8 -*-
"""Crawl Baidubaike's info.

python: 3.6.7
beautifulsoup4: 4.7.1
requests: 2.18.4

Copyright 2019-02-07 @lifanxin
"""
import requests
from bs4 import BeautifulSoup
from bs4 import SoupStrainer


class BaiduBaike:
    """Crawl info from Baidubaike."""
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                    AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/71.0.3578.98 Safari/537.36',
    }
    baike_url = 'https://baike.baidu.com/item'
    param_dicts = {}

    def __init__(self, keyword):
        """
        Init the spider.

        Parameters:
            keyword - what you want to ask.
        """
        self.url = '{}/{}'.format(BaiduBaike.baike_url, keyword)

    def get_response(self):
        """Send request, get response, raise exceptions."""
        try:
            response = requests.get(self.url,
                                    headers=BaiduBaike.headers,
                                    params=BaiduBaike.param_dicts,
                                    timeout=10)
            if response.raise_for_status() is None:
                response.encoding = response.apparent_encoding
                return response
        except requests.exceptions.RequestException:
            raise

    def simple_parse_response(self, response):
        """
        Parse response from label <div class="main-content">.
        it's easy, but catch too much useless info.
        """
        soup = BeautifulSoup(response.text, 'lxml',
                             from_encoding=response.encoding)
        main_content = soup.find('div', class_='main-content')
        return main_content.get_text('\n', strip=True)

    def detailed_parse_response(self, response):
        """
        Parse response into four part.
        Of course, they are all included in <div class="main-content">.

        title: the response title.
        basic_info: the basic info is made into form in the original web.
        content(paras): the main content in the original web.
        references(reference_lists): the news links title at the bottom of
        the original web.
        """
        part_response = SoupStrainer('div', class_='main-content')
        soup = BeautifulSoup(response.text, 'lxml',
                             parse_only=part_response,
                             from_encoding=response.encoding)
        title = soup.find('dd', class_='lemmaWgt-lemmaTitle-title')
        basic_info = soup.find('div', class_='basic-info cmn-clearfix')
        paras = soup('div', class_='para', attrs={'label-module': 'para'})
        # paras include summary
        # summary = soup.find('div', class_='lemma-summary')
        content = ''.join(para.get_text('\n', strip=True) for para in paras)
        reference_lists = soup('a', rel='nofollow', class_='text')
        references = '\n'.join(reference.get_text('\n', strip=True)
                               for reference in reference_lists)
        return title.get_text('\n', strip=True) \
            + basic_info.get_text('\n', strip=True) + content + references


# test
if __name__ == '__main__':
    b = BaiduBaike('马云')
    response = b.get_response()
    text = b.detailed_parse_response(response)
    with open('test.txt', 'w') as f:
        f.write(text)
    print(10*'*' + '\ndown!\n' + 10*'*')
