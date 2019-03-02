# -*- coding: utf-8 -*-
"""Multi-tasks.

@python: 3.6.7
"""

from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from multiprocessing import Process, Manager

from work.spiders.baidu import Baidu
# from work.spiders.wiki import Wiki


class Crawler:

    def __init__(self, spider, keywords):
        self.maxthreads = 8
        self.maxprocesses = 4
        self.keywords = keywords
        self.length = len(keywords) if keywords is not None else 0
        self.threads = self.maxthreads \
            if self.length > self.maxthreads else self.length
        self.spider = spider

    def do_job(self, res):
        if self.threads == 0:
            return

        with ThreadPoolExecutor(self.threads) as executor:
            th_fs = executor.map(self.spider.get_response,
                                 [keyword for keyword in self.keywords])

        with ProcessPoolExecutor(self.maxprocesses) as executor:
            pr_fs = executor.map(self.spider.parse_response,
                                 [response for response in th_fs
                                  if response])
        str = ''
        for txt in pr_fs:
            if txt:
                str += txt
        if not str.strip():
            str = ' '.join(self.keywords)
        res.append(str)


# do multi-work
def working(ch_words,  eg_words):
    ch_crawler = Crawler(Baidu(), ch_words)
    # eg_crawler = Crawler(Wiki(), eg_words)
    print(ch_crawler.threads)
    # print(eg_crawler.threads)

    m = Manager()
    res = m.list()
    ch_p = Process(target=ch_crawler.do_job, args=(res, ))
    # eg_p = Process(target=eg_crawler.do_job, args=(res, ))
    ch_p.start()
    # eg_p.start()
    ch_p.join()
    # eg_p.join()

    text = ' '.join(res)
    print('got text length: {}'.format(len(text)))
    return text


# test
if __name__ == '__main__':
    # from baidu import Baidu
    # from wiki import Wiki

    import time
    bt = time.time()

    eg = ['']
    ch = ['中国']
    text = working(ch, eg)
    # print(text)
    print(text[:-1000])

    et = time.time()
    print('time: {}'.format(et - bt))
