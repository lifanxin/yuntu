# -*- coding: utf-8 -*-
"""Do work."""

import re
import time

from work.spiders import crawler
from work.wcloud import Wcloud
from work.scissors import Scissors
from auto_spiders.db import sqldb


def clear_input(input):
    """Choose something we need."""
    if not input:
        return

    # match Chinese, character, number, the space between the string
    list = re.findall(r"[\u4E00-\u9FA5A-Za-z0-9 ]", input.strip())
    str = ''.join(list)
    return str


def handle_eg(str):
    eg_str = re.findall(r"[A-Za-z ]", str)
    if not eg_str:
        return
    words = ''.join(eg_str)

    return list(words.split(' '))


def handle_ch(str):
    # number belong to ch_str
    keynums = 10
    ch_str = re.findall(r"[\u4E00-\u9FA50-9 ]", str)
    if not ch_str:
        return
    words = ''.join(ch_str)

    scissors = Scissors()
    if len(words) > 10:
        # too long for search, go to get keywords
        s_key = scissors.get_keywords(words, keynums, False)
    else:
        s_key = scissors.cut_words(words)

    # Remove space in s_key
    k_list = [keyword for keyword in s_key.split('/')
              if not keyword.isspace()]

    return k_list


def do_in_db(ch_words):
    db = sqldb.DB()
    for word in ch_words:
        keywords = db.select_info('company', word)
        if keywords:
            return dict(eval(keywords[0]))
    return


def do_in_crawler(ch_words):
    scissors = Scissors()
    keynums = 150

    start = time.time()
    text = crawler.working(ch_words)
    # count time
    end = time.time()
    print('crawl_time: {}'.format(end - start))

    ch_text = ''.join(re.findall(r"[\u4E00-\u9FA50-9 ]", text))
    keywords = scissors.get_keywords(ch_text, keynums, True)

    return keywords


def start(input):
    bt = time.time()

    str = clear_input(input)
    if not str:
        return

    ch_words = handle_ch(str)
    # eg_words = handle_eg(str)
    print(ch_words)
    db_start = time.time()
    keywords = do_in_db(ch_words)
    db_end = time.time()
    print('db time: {}'.format(db_end - db_start))

    if not keywords:
        keywords = do_in_crawler(ch_words)

    start = time.time()
    # eg_text = ''.join(re.findall(r"[A-Za-z ]", text))
    cloud = Wcloud('girl.jpeg', 'SourceHanSerif/SourceHanSerifK-Light.otf')
    # print(ch_list)
    # print(eg_text[:100])
    no_none = cloud.make_it(keywords)
    if not no_none:
        return
    b64_str = cloud.img_to_b64()
    # count time
    cloud_time = time.time()
    print('cloud_time: {}'.format(cloud_time - start))

    et = time.time()
    print('all time: {}'.format(et - bt))

    return b64_str


# test
if __name__ == '__main__':
    # from spiders import crawler
    # from wcloud import Wcloud
    # from scissors import Scissors

    test1 = '我我我们英雄联盟的班德尔城 德玛西亚之力'
    test2 = "英雄联盟的班德尔城 德玛西亚之力"
    s = Scissors()
    t = s.get_keywords(test1, 50, False)
    print(t)
    # print(judge_input(test1))
