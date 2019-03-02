# -*- coding: utf-8 -*-
"""Leader, collect job in here."""

import re
import time

from worker import crawler
from worker.maker import Maker
from worker.scissors import Scissors
from auto_spiders.db import sqldb


class Leader:

    def __init__(self):
        self.input_keynums = 10
        self.make_keynums = 200
        self.table_name = 'company'
        self.img = 'girl.jpeg'
        self.font = 'SourceHanSerif/SourceHanSerifK-Light.otf'
        self.scissors = Scissors()

    def clear_input(self, user_input):
        """Choose something we need."""
        if not user_input:
            return

        # match Chinese, character, number, the space between the string
        singel_word = re.findall(r"[\u4E00-\u9FA5A-Za-z0-9 ]",
                                 user_input.strip())
        clear_user_input = ''.join(singel_word)
        return clear_user_input

    # no use for now
    # def handle_eg(str):
    #     eg_str = re.findall(r"[A-Za-z ]", str)
    #     if not eg_str:
    #         return
    #     words = ''.join(eg_str)

    #     return list(words.split(' '))

    def handle_ch(self, string):
        # number belong to ch_str
        single_str = re.findall(r"[\u4E00-\u9FA50-9 ]", string)
        if not single_str:
            return
        ch_str = ''.join(single_str)

        if len(ch_str) > self.input_keynums:
            # too long for search, go to get keywords
            words = self.scissors.get_keywords(ch_str,
                                               self.input_keynums, False)
        else:
            words = self.scissors.cut_words(ch_str)

        # Remove space in s_key
        search_keywords = [word for word in words.split('/')
                           if not word.isspace()]

        return search_keywords

    def search_from_db(self, search_keywords):
        # return list
        try:
            db = sqldb.DB()
            keywords_list = []
            for keyword in search_keywords:
                company_keywords = db.select_info(self.table_name, keyword)
                if not company_keywords:
                    continue
                # change str into list
                keywords_list.append(eval(company_keywords[0]))

            cloud_keywords = sum(keywords_list, [])
            return cloud_keywords
        except Exception as e:
            print('search from db error: {}'.format(e))
            return
        finally:
            db.close()

    def search_from_crawler(self, search_keywords):
        # return list
        text = crawler.working(search_keywords)
        ch_text = ''.join(re.findall(r"[\u4E00-\u9FA50-9 ]", text))
        cloud_keywords = self.scissors.get_keywords(ch_text,
                                                    self.make_keynums, True)

        return cloud_keywords

    def start(self, user_input):
        bt = time.time()

        leader = Leader()
        clear_user_input = leader.clear_input(user_input)
        if not clear_user_input:
            return
        search_keywords = leader.handle_ch(clear_user_input)
        print('search keywords: {}'.format(search_keywords))

        db_start = time.time()
        cloud_keywords = leader.search_from_db(search_keywords)
        db_end = time.time()
        print('db time: {}'.format(db_end - db_start))

        if not cloud_keywords:
            crawler_start = time.time()
            print('search fromd db fail, get search from internet')
            cloud_keywords = leader.search_from_crawler(search_keywords)
            crawler_end = time.time()
            print('crawler time: {}'.format(crawler_end - crawler_start))

        maker_start = time.time()
        maker = Maker(self.img, self.font)
        no_none = maker.make_it(cloud_keywords)
        if not no_none:
            return
        b64_str = maker.img_to_b64()
        maker_end = time.time()
        print('maker time: {}'.format(maker_end - maker_start))

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
