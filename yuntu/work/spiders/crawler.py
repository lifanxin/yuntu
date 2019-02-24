# -*- coding: utf-8 -*-
"""Multi-tasks.

@python: 3.6.7
"""

import re
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

from work.spiders.baidu import Baidu


class Crawler:

    def __init__(self, keywords):
        self.maxthreads = 8
        self.maxprocesses = 4
        self.keywords = keywords
        self.length = len(keywords)
        self.threads = self.maxthreads \
            if self.length > self.maxthreads else self.length
        self.spider = Baidu()

    def working(self):
        with ThreadPoolExecutor(self.threads) as executor:
            th_fs = executor.map(self.spider.get_response,
                                 [keyword for keyword in self.keywords])

        with ProcessPoolExecutor(self.maxprocesses) as executor:
            pr_fs = executor.map(self.spider.parse_response,
                                 [response for response in th_fs
                                  if response])

        txt = ''
        for text in pr_fs:
            if text:
                clear_txt = re.findall(r"[\u4E00-\u9FA5A-Za-z ]", text)
                txt += ''.join(clear_txt)
        print('got text length: {}'.format(len(txt)))
        if not txt:
            return ''.join(self.keywords)
        return txt


# test
if __name__ == '__main__':
    test = ['斗鱼', '白鹭', '中国']
    c = Crawler(test)
    text = c.working()
    print(len(text))
