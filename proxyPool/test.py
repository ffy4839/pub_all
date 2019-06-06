#!-*- coding:utf-8 -*-
import requests
import json
import time
import os
from fake_useragent import UserAgent
from lxml import etree
import random


def del_removel(data):
    #str2list
    if isinstance(data,str):
        data = data.strip('\n').split('\n')
    #根据nums排序
    func = lambda x: int(x.split(';')[0])
    data.sort(key=func, reverse=True)
    #去重
    data = list(set(data))
    data_ip = [i.split(';')[1] for i in data]
    nums = [data_ip.index(i) for i in list(set(data_ip))]
    data = [data[i] for i in nums]
    # 根据nums排序
    data.sort(key=func, reverse=True)
    return data

PATH = os.getcwd() + os.path.sep + 'proxyPool.txt'
t1 = time.time()
with open(PATH, 'r') as f:
    if f.readable():
        data = f.read().strip('\n')
    else:
        data = 'Err'
x = del_removel(data)
print(len(x),x)
t2 = time.time()
print(t2 - t1)

