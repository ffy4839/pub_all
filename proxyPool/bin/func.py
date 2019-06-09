import time
from run import *


def get_time(st = '%Y-%m-%d %H:%M:%S'):
    return time.strftime(st,time.localtime(time.time()))



def write_data(data, mode='a'):
    if isinstance(data,str):
        data = [data]

    for i in data:
        with open(PATH, mode) as f:
            f.write(i + '\n')


def read_all(mode='r'):
    with open(PATH, mode) as f:
        if f.readable():
            return f.read().strip('\n')


def del_removel_get():
    # str2list
    data = read_all()
    if isinstance(data, str):
        data = data.strip('\n').split('\n')
    # 根据nums排序
    func = lambda x: int(x.split(';')[0])
    data.sort(key=func,)
    # 去重
    data = list(set(data))
    data_ip = [i.split(';')[1] for i in data]
    nums = [data_ip.index(i) for i in list(set(data_ip))]
    data = [data[i] for i in nums]
    # 根据nums排序
    data.sort(key=func, reverse=True)
    return data


def del_removel_check():
    # str2list
    data = read_all()
    if isinstance(data, str):
        data = data.strip('\n').split('\n')
    # 根据nums排序
    func = lambda x: int(x.split(';')[0])
    data.sort(key=func, reverse=True)
    # 去重
    data = list(set(data))
    data_ip = [i.split(';')[1] for i in data]
    nums = [data_ip.index(i) for i in list(set(data_ip))]
    data = [data[i] for i in nums]
    # 根据nums排序
    data.sort(key=func, reverse=True)
    return data

if __name__ == '__main__':
    print(get_time())