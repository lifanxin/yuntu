# -*- coding: utf-8 -*-
"""Crawl info from kanzhun."""

import requests
from bs4 import BeautifulSoup


class Kanzhun:

    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                    AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/71.0.3578.98 Safari/537.36',
        }
        # self.link = 'https://www.kanzhun.com/plc52p1.html?'
        # https://www.kanzhun.com/plc52p10.html?ka=paging10
        self.param_dicts = {
            'ka': None
        }

    def get_one_page(self, number):
        # ka=paging1
        self.link = 'https://www.kanzhun.com/plc52p{}.html?'.format(number)
        self.param_dicts['ka'] = 'paging{}'.format(number)
        print('Kanzhun spider get start...\ncatch page: {}'.format(number))

        try:
            res = requests.get(self.link,
                               headers=self.headers,
                               params=self.param_dicts,
                               timeout=9)
            if res.raise_for_status() is None:
                res.encoding = res.apparent_encoding
                soup = BeautifulSoup(res.text, 'lxml')
                company_results = soup.find('ul', class_='company_result')          
                for company in company_results.find_all('li'):
                    try:
                        tag = company.find('div')

                        company_name = tag.find('a').get_text()
                        company_info = tag.find('p') \
                                          .get_text() \
                                          .replace('\n', '')
                        score_and_average_wage = company.find('dl') \
                                                        .get_text() \
                                                        .replace('\n', ' ') \
                                                        .replace('\xa0', ' ')

                        yield company_name, \
                            company_info, \
                            score_and_average_wage
                    except Exception:
                        continue
        except Exception:
            return

    # def get_response(self, article_data):
    #     url = article_data[1]

    #     try:
    #         response = requests.get(url,
    #                                 headers=self.headers,
    #                                 timeout=9)
    #         if response.raise_for_status() is None:
    #             response.encoding = response.apparent_encoding
    #             return response
    #     except Exception:
    #         return

    # def parse_response(self, response):
    #     try:
    #         soup = BeautifulSoup(response.text, 'lxml')
    #         article_content = soup.find('script', id='__INITIAL_STATE__')
    #         text = article_content.get_text(' ', strip=True)
    #         if text:
    #             clear_txt = re.findall(r"[\u4E00-\u9FA5 ]", text)
    #             txt = ''.join(clear_txt)
    #             return txt
    #     except Exception:
    #         return


# test
if __name__ == '__main__':
    k = Kanzhun()
    company_name = []
    for i in range(1, 11):
        res = k.get_one_page(i)
        for data in res:
            # name: data[0], info: data[1], score_and_average_wage: data[2]
            company_name.append(data[0])

    with open('company.txt', 'a+') as f:
        for name in company_name:
            f.write('\n' + name)
