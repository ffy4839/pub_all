import requests
import json
import time
import os
from fake_useragent import UserAgent
from lxml import etree
import random
from multiprocessing import Pool

MAX = 100
MIN = 0

PATH = os.getcwd() + os.path.sep + 'proxyPool.txt'
UA = UserAgent()
RETRY = 3
PAGES = 5


class main():
    def __init__(self):
        pass

    def run(self):
        pass

    def check_isfile(self):
        if os.path.exists(PATH):
            if os.path.isfile(PATH):
                return True

    def del_removel(self, data):
        data = data.strip('\n').split('\n')
        func = lambda x:int(x.split(';')[0])
        data = list(set(data.sort(data,key=func,reverse=True)))
        data_ip = [i.split(';')[1] for i in data]
        # data_nums = [i.split(';')[0] for i in data]
        nums = [data_ip.index(i) for i in list(set(data_ip))]
        return [data[i] for i in nums]



class ProxyTxt():
    def __init__(self):
        pass

    def write_line(self, data, mode='a'):
        with open(PATH,mode) as f:
            f.write(data+'\n')

    def read_all(self, mode='r'):
        with open(PATH, mode) as f:
            if f.readable():
                return f.read().strip('\n')


class ProxyGet():
    def __init__(self):
        self.url_list = []
        self.Err_url_list = []
        self.get_urls()

    def run(self):
        pass

    def get_proxy(self,data):
        data = data.split(';')
        parse = 'self.crawl_' + data[0]
        url = data[1]
        headers = {
            'User-Agent': UA.random
        }
        n = RETRY
        while n:
            try:
                time.sleep(random.randint(10,30)*0.1)
                re = requests.get(url,headers)
                if re.status_code == 200:
                    return eval(parse)(re)
            except Exception as e:
                self.Err_url_list.append(data)
                print(e,'\n',url)
            finally:
                n-=1

    def get_urls(self, pages=5):
        base_url = {
            'kuaidaili': 'https://www.kuaidaili.com/free/inha/{}/'
        }
        for key in base_url.keys():
            data_func = lambda x: '{name};{url}'.format(name=key,url=base_url[key].format(x))
            self.url_list += [data_func(i) for i in range(1,pages+1)]


    def crawl_kuaidaili(self, response):
        result = etree.HTML(response.text)
        com = '//*[@id="list"]/table/tbody/tr/td[@data-title = "{}"]/text()'
        ip = result.xpath(com.format('IP'))
        port = result.xpath(com.format('PORT'))
        ipport = zip(ip, port)
        func = lambda x:'10;{}:{}'.format(x[0],x[1])
        return [func(i) for i in ipport]


class ProxyUpdata():
    def __init__(self):
        self.url_list = []
        self.over_list = []
        self.txt = ProxyTxt()

    def run(self):
        if not self.url_list:
            self.get_url_list()
        # pool = Pool(10)
        # p = pool.map(self.try_get,self.url_list)
        # p.close()
        # p.join()
        # for i in self.over_list:
        #     self.txt.write_line(i)


    def get_url_list(self):
        data = self.txt.read_all()
        self.url_list = data.split('\n')

    def try_get(self,data,url='https://httpbin.org/get'):
        num = int(data.split(';')[0])
        ipport = data.split(';')[1]
        proxies = {
            'http':ipport,
            'https':ipport,
        }
        try:
            time.sleep(random.randint(10, 50) * 0.1)
            res = requests.get(url=url, proxies=proxies)
            if res.status_code == 200:
                data = json.loads(res.text)
                recv_ip = data['origin'].split(',')[0]
                send_ip = ipport.split(':')[0]
                print(recv_ip, send_ip)
                if send_ip == recv_ip:
                    if num != MAX:
                        num += 1

        except Exception as e:
            if num != 0:
                num-=1
            print(e, ipport)
        self.over_list.append('{};{}'.format(str(num), data.split(';')[1]))



if __name__ == '__main__':
    up = ProxyUpdata()
    up.run()