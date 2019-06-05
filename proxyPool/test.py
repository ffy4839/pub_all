#!-*- coding:utf-8 -*-
import requests
import json
import time
import os
from fake_useragent import UserAgent
from lxml import etree
import random


PATH = os.getcwd() + os.path.sep + 'proxyPool.txt'

with open(PATH, 'r') as f:
    if f.readable():
        data = f.read().strip('\n')
    else:
        data = 'Err'

print(data)