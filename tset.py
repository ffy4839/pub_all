#!-*- coding:utf-8 -*-
import time
import json
from fake_useragent import UserAgent
#
#
# ip = ['94.191.22.17', '59.62.26.49', '219.159.38.207', '61.164.39.67', '59.32.37.73', '60.2.44.182', '47.111.8.157', '182.139.111.83', '47.100.21.174', '163.204.240.128', '36.248.132.62', '60.13.42.234', '113.117.67.100', '120.79.172.37', '121.204.150.218']
# port = ['8118', '9000', '56210', '53281', '3128', '39185', '80', '9000', '8021', '9999', '9999', '9999', '9999', '8118', '8118']
# last_time = ['2019-06-03 23:31:01', '2019-06-03 22:31:01', '2019-06-03 21:31:00', '2019-06-03 20:31:00', '2019-06-03 19:30:59', '2019-06-03 18:30:55', '2019-06-03 17:30:59', '2019-06-03 16:30:58', '2019-06-03 15:31:01', '2019-06-03 14:31:01', '2019-06-03 13:31:01', '2019-06-03 12:30:58', '2019-06-03 11:31:00', '2019-06-03 10:30:59', '2019-06-03 09:31:01']

pp = []
for i in range(1, 21):
    pp.append('com{}'.format(i))


def st(x): return 'com{}'.format(x)


print([st(i) for i in range(1, 21)])