# -*- coding: utf-8 -*-
"""Cut words from data.

data can be user's input or spider info.
return string or None.
"""

from os import path

import jieba
import jieba.analyse


class Scissors:

    def __init__(self):
        self.CURRENT_PATH = path.dirname(path.abspath(__file__))
        self.NW_PATH = path.join(self.CURRENT_PATH, 'words/wc_cn/newwords.txt')
        self.SW_PATH = path.join(self.CURRENT_PATH,
                                 'words/wc_cn/stopwords.txt')
        # add user dict
        jieba.load_userdict(self.NW_PATH)  # must before jieba.enable_parallel
        jieba.enable_parallel(4)
        # Setting up parallel processes: 4,
        # not allow in windows,some editor also can't support,
        # do it in the terminal.

    def cut_words(self, words):
        """Cut short words."""
        if len(words) > 1:
            guess_words = jieba.cut_for_search(words)
            return '/'.join(guess_words)
        return words

    def get_keywords(self, sentence, maxwords, weight):
        """Get keywords from long sentence."""
        # add stop words
        jieba.analyse.set_stop_words(self.SW_PATH)
        keywords = jieba.analyse.extract_tags(sentence, topK=maxwords,
                                              withWeight=weight)

        if weight:
            return keywords
        return '/'.join(keywords)


# def jieba_parse_txt(text, path):
#     """Chinese text!"""
#     # txt = open(self.text_path, 'rb').read()
#     liststr = '/ '.join(jieba.cut(text, cut_all=False))

#     with open(s_path, 'rb') as f_stop:
#         f_stop_text = f_stop.read()
#         f_stop_seg_list = f_stop_text.splitlines()

#     mywordlist = (myword for myword in liststr.split('/')
#                   if not (myword.strip() in f_stop_seg_list)
#                   and len(myword.strip()) > 1)

#     return ' '.join(mywordlist)


# def process_text(text):

#     # stopwords = set([i.lower() for i in self.stopwords])

#      # noqa: F821
#     # flags = (re.UNICODE if sys.version < '3' and type(text) is unicode
#     #             else 0)
#     regexp = r"\w[\w']+"

#     words = re.findall(regexp, text, 0)
#     # remove stopwords
#     words = [word for word in words]
#     # remove 's
#     words = [word[:-2] if word.lower().endswith("'s") else word
#                 for word in words]
#     # remove numbers
#     words = [word for word in words if not word.isdigit()]

#     return words


# test
if __name__ == '__main__':
    test = "英雄联盟的班德尔城得得得得的得的德玛西亚之力"
    scissors = Scissors()
    print(scissors.cut_words(test))
    print(scissors.get_keywords(test, 10))

    # import re
    # import time
    # bt = time.time()
    # s_path = path.join(scissors.CURRENT_PATH, 'words/wc_cn/stopwords.txt')
    # t_path = path.join(scissors.CURRENT_PATH, 'mayun.txt')
    # w_path = path.join(scissors.CURRENT_PATH, 'new.txt')
    # # with open(t_path, 'r') as f:
    # #     txt = f.read()
    # # st = scissors.get_keywords(txt)
    # # print(type(st))
    # # print(re.findall(r"[\u4E00-\u9FA5A-Za-z0-9/]", st))
    # # # for i in st:
    # # #     if re.match(r"^[\u4E00-\u9FA5A-Za-z]+$", i):
    # # #         print(i)

    # # at = time.time()

    # # print('time: {}'.format(at-bt))
    # import time
    # bt = time.time()
    # with open(w_path, 'r') as f:
    #     txt = f.read()
    # print(process_text(txt))
    # at = time.time()
    # print('time: {}'.format(at - bt))
