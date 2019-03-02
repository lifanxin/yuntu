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
        self.link = 'https://www.kanzhun.com'
        self.param_dicts = {
            'ka': None
        }
        self.proxies = {
            'https': '162.105.87.211:8118'
        }

    def get_host_city(self):
        url = '{}/companyl/search/?'.format(self.link)
        self.param_dicts['ka'] = 'banner-com'

        print(url)
        try:
            res = requests.get(url,
                               headers=self.headers,
                               params=self.param_dicts,
                               proxies=self.proxies,
                               timeout=9)
            print(res.url)
            print(res.status_code)
            if res.raise_for_status() is None:
                res.encoding = res.apparent_encoding
                soup = BeautifulSoup(res.text, 'lxml')
                host_citys = soup.find('div', class_='host_city')
                for host_city in host_citys.find_all('a', class_='links'):
                    try:
                        city_name = host_city.get_text()
                        city_html = host_city.get('href') \
                                             .replace('p1.html', '')
                        city_ka = host_city.get('ka')

                        yield city_name, \
                            city_html, \
                            city_ka
                    except Exception:
                        continue
        except Exception:
            return

    def get_one_page(self, host_city_info, number):
        internet_company_code = 'c52'
        page = 'p{}.html'.format(number)
        url = '{}{}{}{}?'.format(self.link, host_city_info[1],
                                 internet_company_code, page)
        self.param_dicts['ka'] = 'paging{}'.format(number)
        print('Kanzhun spider get start...\n'
              'catch city: {}, page {}'.format(host_city_info[0], number))

        try:
            res = requests.get(url,
                               headers=self.headers,
                               params=self.param_dicts,
                               proxies=self.proxies,
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


# test
if __name__ == '__main__':
    import time

    k = Kanzhun()
    host_cities_info = k.get_host_city()

    company_name = []
    for host_city_info in host_cities_info:
        mark = '# {}'.format(host_city_info[0])
        company_name.append(mark)
        for i in range(1, 11):
            time.sleep(2)  # too quick will be refuse
            res = k.get_one_page(host_city_info, i)
            for data in res:
                # name: data[0], info: data[1], score_and_average_wage: data[2]
                company_name.append(data[0])
                # print(data)

    with open('company.txt', 'a+') as f:
        for name in company_name:
            f.write('\n' + name)
