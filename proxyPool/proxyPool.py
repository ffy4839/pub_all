import requests
import json
import time
import os
from fake_useragent import UserAgent
from lxml import etree


PATH = os.getcwd() + os.path.sep
UA = UserAgent()

class save():
    def __init__(self):
        pass

    def save_proxy(self, data, mod='txt'):
        pass

    def txt_mod(self, data):
        pass




class craw():
    def __init__(self):
       self.url_list = []

    def get_proxy(self,data):
        data = data.split(';')
        parse = 'self.crawl_' + data[0]
        url = data[1]
        headers = {
            'User-Agent': UA.random
        }
        try:
            re = requests.get(url,headers)
            if re.status_code == 200:
                return eval(parse)(re)

        except Exception as e:
            print(e,'\n',url)

        


    def get_urls(self, pages=5):
        base_url = {
            'kuaidaili': 'https://www.kuaidaili.com/free/inha/{}/'
        }
        for key in base_url.keys():
            data_func = lambda x: '{name};{url}'.format(name=key,url=base_url[key].format(x))
            self.url_list += [data_func(i) for i in range(1,pages+1)]


    def crawl_kuaidaili(self, response):
        result = etree.HTML(response.text)
        com = ''
        ip =
        port =
        ipport = zip(ip, port)
