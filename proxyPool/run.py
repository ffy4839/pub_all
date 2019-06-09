import os
import time


LEVEL_MAX = 100
LEVEL_MIN = 0
LEVEL_INIT = 10

PATH = os.path.dirname(os.getcwd()) + os.path.sep + 'docs'+ os.path.sep +'proxyPool.txt'

RETRY = 3
PAGES = 10

GET_INTERVAL = 6 #获取proxy间隔 h
CHECK_INTERVAL = 3 #检查proxy有效性间隔 h

