# -*- coding: utf-8 -*-
"""Crawler, collect info in here.

@python: 3.6.7
"""

from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

from worker.spiders.baidu import Baidu
# from worker.spiders.wiki import Wiki


class Crawler:

    def __init__(self, keywords):
        self.maxthreads = 8
        self.maxprocesses = 5
        self.keywords = keywords
        self.length = len(keywords) if keywords is not None else 0
        self.threads = self.maxthreads \
            if self.length > self.maxthreads else self.length

    def do_job(self, spider):
        if self.threads == 0:
            return

        with ThreadPoolExecutor(self.threads) as executor:
            th_fs = executor.map(spider.get_response,
                                 [keyword for keyword in self.keywords])

        with ProcessPoolExecutor(self.maxprocesses) as executor:
            pr_fs = executor.map(spider.parse_response,
                                 [response for response in th_fs
                                  if response], chunksize=2)

        string = [txt for txt in pr_fs if txt]
        text = ' '.join(string)
        return text


# do multi-work
def working(search_keywords):
    print('search list: {}'.format(search_keywords))
    crawler = Crawler(search_keywords)
    spider = Baidu()

    text = crawler.do_job(spider)
    print('got text length: {}'.format(len(text)))
    return text


# test
if __name__ == '__main__':
    pass
    # from baidu import Baidu
    # from wiki import Wiki

    # import time
    # bt = time.time()

    # eg = ['']
    # ch = ['中国']
    # text = working(ch, eg)
    # # print(text)
    # print(text[:-1000])

    # et = time.time()
    # print('time: {}'.format(et - bt))
