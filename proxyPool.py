#!-*- coding:utf-8 -*-
import requests
from fake_useragent import UserAgent
import time
import os
from lxml import etree
from multiprocessing import Pool
import random


PATH = os.getcwd() + os.path.sep

def get_time(st='%Y-%m-%d %H:%M:%S'):
    return time.strftime(st,time.localtime(time.time()))

def save_data(data, name='proxyPool'):
    path = PATH + name + '.txt'
    try:
        with open(path,'a') as f:
            f.write(data)
    except Exception as e:
        print('Err: {}\n{}'.format(data, e))

def read_data(name='proxyPool'):
    path = PATH + name + '.txt'
    try:
        with open(path,'r') as f:
            data = f.read()
            return data
    except Exception as e:
        print('Err: {}'.format(e))


class get_IP():
    def __init__(self):
        self.ip_port = []

    def url_list(self,n=5, base_url='https://www.kuaidaili.com/free'):
        url_list = []
        for i in range(1,n+1):
            url_list.append('{}/inha/{}/'.format(base_url,str(i)))
        return url_list

    def get_response(self, url):
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        }
        try:
            time.sleep(random.randint(1,10) * 0.1)
            response = requests.get(url,headers=header)
            return response
        except Exception as e:
            print(e)

    def parse(self,url):
        response = self.get_response(url)
        if response:
            lxml_res = etree.HTML(response.text)
            res_com = '//*[@id="list"]/table/tbody/tr/td[@data-title = "{}"]/text()'
            ip = lxml_res.xpath(res_com.format('IP'))
            port = lxml_res.xpath(res_com.format('PORT'))
            last_time = lxml_res.xpath(res_com.format('最后验证时间'))
            c = zip(ip, port, last_time)
            dict_c = {}
            for i in c:
                times = str(int(time.mktime(time.strptime(i[2], '%Y-%m-%d %H:%M:%S'))))
                dict_c[times] = '{}:{}'.format(i[0], i[1])

            for key in dict_c.keys():
                save_data('{},{}\n'.format(key,dict_c[key]))
                print('{} got it: {}'.format(get_time(),url))
        else:
            print('Err  {}'.format(url))


if __name__ == '__main__':
    get_page = get_IP()
    url_list = get_page.url_list(5)
    print(url_list)
    pool = Pool()
    pool.map(get_page.parse, url_list)
    pool.close()
    pool.join()
    print('over')
