# -*- coding: utf-8 -*-
"""Maker, make word cloud in here."""

from os import path
import base64
import io

from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
from scipy.misc import imread


class Maker:
    """Generate wordcloud!"""

    def __init__(self, from_image_file, from_font_file):
        """
        Init object.

        Parameters:
            from_image_file - choose a image as a mask.
            from_font_file - choose a font for wordcloud.
        """
        self.path = path.dirname(path.abspath(__file__))
        self.image_path = path.join(self.path, 'image', from_image_file)
        self.font_path = path.join(self.path, 'words/fonts', from_font_file)
        self.set_wc()  # init setting

    def set_wc(self):
        """Set WordCloud parameters!"""
        self.mask = imread(self.image_path)
        self.image_colors_byImg = ImageColorGenerator(self.mask)
        self.wc = WordCloud(
            font_path=self.font_path,
            background_color=None,
            max_words=500,
            mask=self.mask,
            max_font_size=66,
            min_font_size=32,
            random_state=0,
            # width=2000,
            # height=860,
            margin=2,
            # contour_width=0,
            # contour_color='steelblue',
            ranks_only=None,
            prefer_horizontal=.9,
            scale=1,
            color_func=lambda *args, **kwargs: (255, 255, 255),
            stopwords=None,
            font_step=1,
            mode="RGBA",
            relative_scaling='auto',
            regexp=None,
            collocations=True,
            colormap=None,
            normalize_plurals=True,
            repeat=True,
        )

    def make_it(self, cloud_keywords):
        if not cloud_keywords:
            return
        self.wc.generate_from_frequencies(dict(cloud_keywords))
        return True

    # def make_it(self, ch_list, eg_text):
    #     eg_dict = self.wc.process_text(eg_text)
    #     print(eg_dict)
    #     all_dict = {**dict(ch_list), **eg_dict}
    #     if not all_dict:
    #         return
    #     self.wc.generate_from_frequencies(all_dict)
    #     return 'ok'

    def process_text(self, text):
        self.wc.process_text(text)
        # self.wc.to_html()

    def show_it(self):
        """Show wordcloud by default."""
        plt.imshow(self.wc)
        plt.axis('off')
        plt.show()

    def show_it_colorByImg(self):
        """Show wordcloud, recolor by image."""
        plt.imshow(self.wc.recolor(color_func=self.image_colors_byImg))
        plt.axis('off')
        plt.show()

    def show_origin(self):
        """Show origin image which is chosen as a mask."""
        plt.imshow(self.mask)
        plt.axis('off')
        plt.show()

    def save_it(self, imname):
        # recolor by image color
        # self.wc.recolor(color_func=self.image_colors_byImg)
        filename = '{}.png'.format(imname)
        self.wc.to_file(path.join(self.path, 'data', filename))
        return imname

    # image to base64
    def img_to_b64(self):
        img = self.wc.to_image()
        buf = io.BytesIO()
        img.save(buf, format='png')
        b_data = buf.getvalue()
        b64_str = base64.b64encode(b_data).decode()
        return b64_str


# test
if __name__ == '__main__':
    pass
    # test = "英雄联盟的班德尔城 德玛西亚之力"
    # import jieba
    # list = ' '.join(jieba.cut(test, cut_all=False))

    # import time
    # bt = time.time()
    # # with open('data/test.png', 'rb') as f:
    # #     txt = f.read()
    # # img_code = base64.b64encode(txt)
    # # print(len(img_code))
    # # with open('code.txt', 'wb') as f:
    # #     f.write(img_code)
    # w = Wcloud('girl.jpeg', 'SourceHanSerif/SourceHanSerifK-Light.otf')
    # w.make_it_by_text(list)
    # t = w.img_to_b64()
    # print(t)
    # print(type(t))
    # buf = io.BytesIO()
    # t.save(buf, format='png')
    # b_data = buf.getvalue()
    # base64_str = base64.b64encode(b_data)
    # print(len(base64_str))
    # # str = base64.b64encode(t)
    # # print(len(str))
    # with open('code.txt', 'wb') as f:
    #     f.write(base64_str)
    # # print(len(t[1]))
    # # print(t[1])
    # # w.save_it('nothing')
    # et = time.time()
    # print('use time: {}'.format(et - bt))
