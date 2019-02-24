# -*- coding: utf-8 -*-
"""Do work."""

import re
import time

from work.spiders import crawler
from work.wcloud import Wcloud
from work.scissors import Scissors


def clear_input(input):
    """Choose something we need."""
    if not input:
        return

    # match Chinese, character, number, the space between the string
    list = re.findall(r"[\u4E00-\u9FA5A-Za-z0-9 ]", input.strip())
    str = ''.join(list)
    return str


def judge_input(str):
    keynums = 10

    scissors = Scissors()
    if len(str) > 10:
        # too long for search, go to get keywords
        s_key = scissors.get_keywords(str, keynums, False)
    else:
        s_key = scissors.cut_words(str)

    return s_key


def clear_keys(keywords):
    """Remove space in keywords."""
    k_list = [keyword for keyword in keywords.split('/')
              if not keyword.isspace()]

    return k_list


def start(input):
    bt = time.time()

    str = clear_input(input)
    if not str:
        return

    keywords = judge_input(str)
    k_list = clear_keys(keywords)

    crawl = crawler.Crawler(k_list)
    text = crawl.working()

    scissors = Scissors()
    keynums = 500
    d_words = scissors.get_keywords(text, keynums, True)
    # print(d_words)
    if not d_words:
        return

    cloud = Wcloud('girl.jpeg', 'SourceHanSerif/SourceHanSerifK-Light.otf')
    name = d_words[0][0]
    cloud.make_it(d_words)
    status = cloud.save_it(name)

    et = time.time()
    print('use time: {}'.format(et - bt))

    return status, name


# test
if __name__ == '__main__':
    test1 = '  我  的 '
    test2 = "英雄联盟的班德尔城 德玛西亚之力"
    print(judge_input(test1))
