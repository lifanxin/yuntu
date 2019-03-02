# -*- coding: utf-8 -*-
"""Multi-tasks.

@python: 3.6.7
"""

import concurrent.futures
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from os import path

import jieba.analyse

from ifeng import Ifeng
from people import People
from sina import Sina
from toutiao import Toutiao
from xinhuanet import Xinhuanet


class Crawler:

    def __init__(self):
        self.max_thread = 10  # the most page only have ten links
        self.max_process = 5  # five spiders need to done

    def do_job(self, spider, keyword):
        self.spider = spider
        datas = self.spider.get_news(keyword)

        # multi-threads for networking
        with ThreadPoolExecutor(self.max_thread) as e:
            th_res = e.map(self.spider.get_response,
                           [data for data in datas])

        # multi-processes for parse
        with ProcessPoolExecutor(self.max_process) as e:
            pr_res = e.map(self.spider.parse_response,
                           [response for response in th_res if response],
                           chunksize=2)
        txt = [text for text in pr_res if text]
        return ' '.join(txt)


def parse_words(text):
    jieba.enable_parallel(4)

    # catch keywords
    keywords = jieba.analyse.extract_tags(text, topK=500, withWeight=True)
    return keywords


# do multi-work
def working():
    c = Crawler()
    current_path = path.dirname(path.abspath(__file__))
    company_file = path.join(current_path, 'company', 'company.txt')
    spiders = [Ifeng(), People(), Sina(), Toutiao(), Xinhuanet()]

    with ProcessPoolExecutor(max_workers=c.max_process) as e:
        with open(company_file) as f:
            companies = f.readlines()
        for company in companies:
            tasks = [e.submit(c.do_job, spider, company) for spider in spiders]

            text = [future.result()
                    for future in concurrent.futures.as_completed(tasks) 
                    if future.result()]
            big_text = ' '.join(text)
            yield [company, parse_words(big_text)]


# test
if __name__ == '__main__':
    import time
    start = time.time()
    working()
    end = time.time()

    print('time: {}'.format(end - start))
