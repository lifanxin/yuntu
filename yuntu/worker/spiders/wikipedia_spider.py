# -*- coding: utf-8 -*-
"""Crawl Wiki's info.

python: 3.6.7
beautifulsoup4: 4.7.1
requests: 2.18.4

Copyright 2019-02-09 @lifanxin
"""
import requests
from bs4 import BeautifulSoup
from bs4 import SoupStrainer

import os


class Wikipedia:
    """Crawl info from Wikipedia."""
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                    AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/71.0.3578.98 Safari/537.36',
    }
    Wikipedia_url = 'https://en.wikipedia.org/wiki'
    param_dicts = {}

    def __init__(self, keyword):
        """Init the spider.

        :param keyword: what you want to ask.
        """
        self.url = '{}/{}'.format(Wikipedia.Wikipedia_url, keyword)

    def get_response(self):
        """Send request, get response, raise exceptions."""
        try:
            response = requests.get(self.url,
                                    headers=Wikipedia.headers,
                                    params=Wikipedia.param_dicts,
                                    timeout=10)
            if response.raise_for_status() is None:
                response.encoding = response.apparent_encoding
                return response
        except requests.exceptions.RequestException:
            raise

    def simple_parse_response(self, response):
        """
        Parse response from label <div class="mw-parser-output">.
        it's easy, but catch too much useless info.
        """
        soup = BeautifulSoup(response.text, 'lxml',
                             from_encoding=response.encoding)
        mw_content = soup.find('div', class_='mw-parser-output')
        return mw_content.get_text('\n', strip=True)

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
    b = Wikipedia('Mission: Impossible')
    response = b.get_response()
    text = b.simple_parse_response(response)

    folder_path = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(folder_path, 'words/wiki_simple_test.txt')
    print(file_path)
    with open(file_path, 'w') as f:
        f.write(text)
    print(10*'*' + '\ndown!\n' + 10*'*')
