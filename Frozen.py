import serial
import configparser
import os
import binascii
import sys
import re
import time
import threading


def get_config(sections):
    data = {}
    config = configparser.ConfigParser()
    path = os.getcwd() + os.path.sep
    if 'setConfig.ini' in os.listdir(path):
        config.read(path + 'setConfig.ini', encoding='UTF-8')
        for i in config.items(section=sections):
            data[i[0]] = i[1]
        return data

    else:
        config['configs'] = {}
        # config['configs']['port'] = 'com10'
        config['configs']['baudrate'] = '9600'
        # config['configs']['starttime'] = '190101005955'
        config['configs']['frozen_hour'] = '24'
        config['configs']['frozen_day'] = '3'
        config['configs']['frozen_month'] = '2'
        config['configs']['interval'] = '20'

        with open(path + 'setConfig.ini', 'w') as f:
            config.write(f)
        input('创建成功')
        sys.exit()


config_data = get_config('configs')


def choose_port():
    portin = input('输入端口号（不输入为配置文件端口号）：')
    pp = []
    for i in range(1, 21):
        pp.append('com{}'.format(i))
    if portin in pp:
        return portin
    else:
        return config_data['port']


BAUDRATE = int(config_data['baudrate'])  # 波特率

# STARTTIME = config_data['starttime']  # 开始时间

FROZEN_HOUR_TIMES = int(config_data['frozen_hour'])  # 小时冻结次数
FROZEN_DAY_TIMES = int(config_data['frozen_day'])  # 天冻结次数
FROZEN_MONTH_TIME = int(config_data['frozen_month'])  # 月冻结次数

INTERVAL = int(config_data['interval'])              # 两次设置间隔

PATH = os.getcwd() + os.path.sep + '运行记录.txt'


def save(data):
    '''数据存储'''
    try:
        with open(PATH, 'a') as f:
            f.write(data)
            f.write('\n')
    except Exception as e:
        print('{},存储失败'.format(e))


def quit():
    input('按任意键退出')
    sys.exit()


def timen(d='%Y-%m-%d,%H:%M:%S'):
    return time.strftime(d, time.localtime(time.time()))


class ser(serial.Serial):
    def __init__(self, port):
        super(ser, self).__init__()
        self.port = port
        self.open_ser()

    def open_ser(self):

        self.baudrate = BAUDRATE
        self.timeout = 0.5
        self.open()

    def send(self, data):
        '''串口发送数据'''
        data = binascii.unhexlify(data)
        if self.is_open:
            try:
                self.flushOutput()
                self.write(data)
            except Exception as e:
                err = '{};{},串口发送错误'.format(timen(), e)
                print(err)
                save(err)
                time.sleep(10)
                quit()
        else:
            self.open_ser()

    def recv(self, times=6):
        self.isopened()
        self.flushInput()
        for i in range(times):
            inwaiting = self.in_waiting
            if inwaiting:
                recv = self.read_all()
                return self.recv_parse(recv)
            time.sleep(1)

    def recv_parse(self, data):
        try:
            datas = binascii.hexlify(data).decode('utf-8').upper()

            re_com = re.compile('68.*16')
            datas = re.findall(re_com, datas)[0]

        except:
            try:
                datas = data.decode('ascii')
            except:
                datas = data
        return datas

    def sopen(self):
        if not self.is_open:
            self.open()

    def sclose_ser(self):
        if self.is_open:
            self.close()

    def isclosed(self):
        if self.is_open:
            self.close()

    def isopened(self):
        if not self.is_open:
            self.open()


class pro():
    def __init__(self):
        self.pro = self.initinput()

    def initinput(self):
        xuanze = input('{}\n{}\n{}\n{}'.format(
            '1、民用物联网', '2、商业物联网', '3、自定义', '输入序号选择：'))

        if xuanze == '1':
            ts = '190313010203'
            inp_a = '68 00 00 00 01 00 00 68 04 10 00 {} 16 21 C6 00 {} 3F 16'.format(
                timen('%y%m%d%H%M%S'), ts).replace(' ', '')
            inp_b = ts
        elif xuanze == '2':
            ts = '190313010203'
            inp_a = '68 FF FF FF FF FF FF 68 04 10 00 {} 02 03 AA 00 {} CF 16'.format(
                timen('%y%m%d%H%M%S'), ts).replace(' ', '')
            inp_b = ts
        else:
            inp_a = input('输入发送帧部分：').replace(' ', '')
            inp_b = input('输入帧时间部分：').replace(' ', '')
        try:
            coordinate_set = re.search(inp_b, inp_a).span()
        except:
            coordinate_set = None
        timenow = timen('%y%m%d%H')
        try:
            cc = re.compile(timenow + '.{4}')
            coordinate_time = re.search(cc, inp_a).span()
        except:
            coordinate_time = (0, 0)
        try:
            part_1 = inp_a[:coordinate_time[0]]
            part_2 = inp_a[coordinate_time[1]:coordinate_set[0]]
            part_3 = inp_a[coordinate_set[1]:-4]
            return part_1, part_2, part_3
        except:
            print('数据输入错误,即将退出程序', end='')
            for i in range(5):
                print('.', end='', flush=True)
                time.sleep(1)
            sys.exit()

    def run(self, settime):
        part_1 = self.pro[0]
        part_2 = self.pro[1]
        part_3 = self.pro[2]

        timenow = timen('%y%m%d%H%M%S')
        part = part_1 + timenow + part_2 + settime + part_3
        data = part + self.checkSum(part) + '16'
        return data.upper()

    def checkSum(self, data):
        data = data.replace(' ', '')
        check = 0x00
        L = len(data)
        for i in range(0, L, 2):
            check = int(data[i:(i + 2)], 16) + check
            if check > 0xff:
                check -= 0x100
        check_hex = hex(check)[2:]
        return ('0' * (2 - len(check_hex)) + check_hex).upper()


class setTimeList():
    def __init__(self):
        self.set_struct = '5955'
        self.last_time_list = []

    def run(self, th, td, tm):
        set_time_list = []
        self.creat_formerly_time_list(15)

        time_list = self.last_time_list
        if th != 0:
            while True:
                if th == 0:
                    break
                set_time_list.append(time_list.pop())
                th -= 1
        if td != 0:
            while True:
                if td == 0:
                    break
                get_time = time_list.pop()
                if '23' + self.set_struct in get_time:
                    set_time_list.append(get_time)
                    td -= 1
        if tm != 0:
            while True:
                if tm == 0:
                    break
                # print(len(time_list),tm)
                get_time = time_list.pop()
                # print(get_time)
                if '013123' + self.set_struct in get_time:
                    set_time_list.append(get_time)
                    tm -= 1

                elif '022923' + self.set_struct in get_time:
                    set_time_list.append(get_time)
                    tm -= 1

                elif '022823' + self.set_struct in get_time:
                    # print(set_time_list)
                    if '022923' + self.set_struct not in set_time_list[-1]:
                        set_time_list.append(get_time)
                        tm -= 1

                elif '033123' + self.set_struct in get_time:
                    set_time_list.append(get_time)
                    tm -= 1

                elif '043023' + self.set_struct in get_time:
                    set_time_list.append(get_time)
                    tm -= 1

                elif '053123' + self.set_struct in get_time:
                    set_time_list.append(get_time)
                    tm -= 1

                elif '063023' + self.set_struct in get_time:
                    set_time_list.append(get_time)
                    tm -= 1

                elif '073123' + self.set_struct in get_time:
                    set_time_list.append(get_time)
                    tm -= 1

                elif '083123' + self.set_struct in get_time:
                    set_time_list.append(get_time)
                    tm -= 1

                elif '093023' + self.set_struct in get_time:
                    set_time_list.append(get_time)
                    tm -= 1

                elif '103123' + self.set_struct in get_time:
                    set_time_list.append(get_time)
                    tm -= 1

                elif '113023' + self.set_struct in get_time:
                    set_time_list.append(get_time)
                    tm -= 1

                elif '123123' + self.set_struct in get_time:
                    set_time_list.append(get_time)
                    tm -= 1
        self.result = set_time_list
        return set_time_list

    def creat_formerly_time_list(self, years=12):
        # 创建12年零点
        struct = self.set_struct
        now_time = self.get_now_time()
        now_time = now_time[:8] + struct

        n = years * 365 * 24
        while n:
            self.last_time_list.append(now_time)
            self.last_hour(now_time)
            now_time = self.last_hour(now_time)
            n -= 1

        self.last_time_list.reverse()

    def last_hour(self, intime_str):
        # 获取上一个小时的时间点
        stamptime = self.str_time2stamp_time(intime_str)
        last_stamptime = stamptime - 60 * 60
        outtime_str = self.stamp_time2str_time(last_stamptime)
        # print(outtime_str)
        return outtime_str

    def str_time2stamp_time(self, strtime, struct='%y%m%d%H%M%S'):
        # 将格式化时间转为时间戳
        return time.mktime(time.strptime(strtime, struct))

    def stamp_time2str_time(self, stamptime, struct='%y%m%d%H%M%S'):
        # 将时间戳转为格式化时间
        return time.strftime(struct, time.localtime(stamptime))

    def get_now_time(self, struct='%y%m%d%H%M%S'):
        return time.strftime(struct, time.localtime(time.time()))

    # def test(self):
    #     #     test_list = []
    #     #     for i in range(20):
    #     #         xx = (random.randint(0, 1000), random.randint(0, 100), random.randint(0, 100))
    #     #         test_list.append(xx)
    #     #     for test in test_list:
    #     #         sum = 0
    #     #         for i in test:
    #     #             sum += i
    #     #         res = self.run(test[0], test[1], test[2])
    #     #         print(len(res), sum)
    #     #         # print()
    #     #         if len(res) == sum:
    #     #             print('OK')

# class set_time():
#     def __init__(self):
#         self.time_list = []
#
#     def run(self, hs, ds, ms):
#         # print('线程1')
#         self.add_timeList()
#         x = self.time_list
#         t = []
#         for y in x:
#             for m in y:
#                 for d in m:
#                     for h in d:
#                         if len(t) > hs or hs == 0:
#                             break
#                         t.append(h)
#                     if len(t) > hs + ds or hs + ds == 0:
#                         break
#                     if len(t) > hs:
#                         t.append(d[0])
#                 if len(t) > ms + hs + ds:
#                     break
#                 if len(t) > hs + ds:
#                     t.append(m[0][0])
#             if len(t) > ms + hs + ds:
#                 break
#         # print(len(t), (ms + ds + hs))
#         # print(t)
#         self.result = t
#         # print('shijinalianbiao chansheng ')
#         return t
#
#     def get_structtime(self, d):
#         return time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(d, '%y%m%d%H%M%S'))
#
#     def add_timeList(self):
#         start_time = self.get_nowtime()
#         end_time = str(int(self.get_year(start_time)) -
#                        11).zfill(2) + start_time[2:]
#         next_time = start_time
#         # print('起始时间：{}，停止时间:{}'.format(self.get_structtime(
#         #     end_time), self.get_structtime(start_time)))
#
#         self.time_list = []
#
#         y = self.get_year(next_time)
#         m = self.get_month(next_time)
#         d = self.get_day(next_time)
#
#         while True:
#             if next_time == end_time:
#                 break
#             y0 = y
#             years = []
#             while True:
#                 if next_time == end_time:
#                     break
#                 if y != y0:
#                     break
#                 m0 = m
#                 months = []
#                 while True:
#                     if next_time == end_time:
#                         break
#                     if m != m0:
#                         break
#                     d0 = d
#                     days = []
#                     while True:
#                         if next_time == end_time:
#                             break
#                         if d != d0:
#                             break
#                         days.append(next_time)
#                         d0 = d
#                         m0 = m
#                         y0 = y
#                         next_time = self.reduce_hour(next_time)
#                         y = self.get_year(next_time)
#                         m = self.get_month(next_time)
#                         d = self.get_day(next_time)
#                     months.append(days)
#
#                 years.append(months)
#             self.time_list.append(years)
#
#     def reduce_hour(self, struct_time):
#         return time.strftime('%y%m%d%H%M%S', time.localtime(
#             time.mktime(time.strptime(struct_time, '%y%m%d%H%M%S')) - 3600))
#
#     def get_nowtime(self,):
#         str_time = time.strftime(
#             '%y%m%d', time.localtime(time.time())) + '005955'
#         return str_time
#
#     def get_year(self, str_time):
#         return str_time[0:2]
#
#     def get_day(self, str_time):
#         return str_time[4:6]
#
#     def get_month(self, str_time):
#         return str_time[2:4]

# class addtime():
#     def __init__(self):
#         self._frozenType = 'hour'
#
#     def changeType(self, inset):
#         dict_type = ['hour','day','month','h','d','m']
#         if inset in dict_type:
#             self._frozenType = inset
#
#     def run(self, addtime):
#         type_all = {
#             'day': self.add_day,
#             'hour': self.add_hour,
#             'month': self.add_month,
#             'h':self.add_hour,
#             'd':self.add_day,
#             'm':self.add_month
#         }
#         return type_all[self._frozenType](addtime)
#
#     def add_day(self,addtime):
#
#         if len(addtime) == 14:
#             d = '%Y%m%d%H%M%S'
#         else:
#             d = '%y%m%d%H%M%S'
#         t = time.mktime(time.strptime(addtime, d))
#         return time.strftime(d, time.localtime(t + 24 * 3600))
#
#     def add_hour(self,addtime):
#
#         if len(addtime) == 14:
#             d = '%Y%m%d%H%M%S'
#         else:
#             d = '%y%m%d%H%M%S'
#         t = time.mktime(time.strptime(addtime, d))
#         return time.strftime(d, time.localtime(t + 3600))
#
#     def add_month(self,addtime):
#
#         if len(addtime) == 12:
#             # d = '%y%m%d%H%M%S'
#             # t = time.mktime(time.strptime(addtime, '%y%m%d%H%M%S'))
#             ty = int('20' + addtime[0:2])
#             tm = int(addtime[2:4])
#         elif len(addtime) == 14:
#             # d = '%Y%m%d%H%M%S'
#             # t = time.mktime(time.strptime(addtime, '%Y%m%d%H%M%S'))
#             ty = int(addtime[0:4])
#             tm = int(addtime[4:6])
#         else:
#             return None
#         if not int(ty) % 4 and int(ty) % 100 or not int(ty) % 400:
#             month_list = [0, 31, 29, 31, 30, 31,
#                           30, 31, 31, 30, 31, 30, 31, 31]
#         else:
#             month_list = [0, 31, 28, 31, 30, 31,
#                           30, 31, 31, 30, 31, 30, 31, 31]
#         for i in range(len(month_list)):
#             month_list[i] = str(month_list[i])
#
#         tm+=1
#         if tm == 13:
#             tm = 1
#             ty+=1
#
#         dd = '{}{}{}{}'.format(str(ty).zfill(2),str(tm).zfill(2),month_list[tm],'235955')
#
#         return dd


class main():
    def __init__(self):

        # self.addtime = addtime()
        self.timeset = setTimeList()
        self.times_n = 0
        self.times_sum = 0

    def run(self):

        p = threading.Thread(target=self.timeset.run, args=(FROZEN_HOUR_TIMES,
                                                            FROZEN_DAY_TIMES,
                                                            FROZEN_MONTH_TIME))
        # xxx = time.time()
        p.start()

        # time_list = self.timeset.run(
        #     FROZEN_HOUR_TIMES,
        #     FROZEN_DAY_TIMES,
        #     FROZEN_MONTH_TIME
        # )
        PORT = choose_port()  # 串口
        self.ser = ser(PORT)
        self.pro = pro()

        p.join()
        # print(time.time()-xxx)
        time_list = self.timeset.result

        # print(time_list)

        self.print_save('\n起始时间：{}，停止时间:{}\n'.format(self.parse_struct_time(
            time_list[-1]), self.parse_struct_time(time_list[0])))

        lasttime = 0

        while True:
            nowtime = time.time()

            if len(time_list) == 0:
                break
            get_time = time_list.pop()  # 本次设置的时间
            p_get_time = self.print_get_time(get_time)  # 格式化本次设置的时间用于打印
            data = self.pro.run(get_time)  # 数据帧
            self.ser.send(data)  # 串口发送
            ll = len(time_list)  # 剩余次数

            sysj = self.shengyushijian(ll, nowtime, lasttime)  # 预计剩余时间
            lasttime = nowtime

            self.print_data(ll, p_get_time, sysj, data)  # 打印存储数据
            self.wait_recv()  # 等待接收

        print('运行结束')
        quit()

    def print_save(self, data):
        print(data)
        save(data)

    def print_data(self, ll, p_get_time, sysj, data):
        p_datas = '剩余次数：{a}, 设置的时间：{b}\n预计剩余时间：{c}\n[{d}], 发送: {e}'.format(
            a=str(ll), b=p_get_time, c=sysj, d=timen(), e=data)
        self.print_save(p_datas)

    def print_get_time(self, x):
        try:
            xs = '20{}-{}-{},{}:{}:{}'.format(
                x[0:2],
                x[2:4],
                x[4:6],
                x[6:8],
                x[8:10],
                x[10:12]
            )
            return xs
        except:
            return '计算错误'

    def shengyushijian(self, data, nowtime, lasttime):
        if lasttime == 0:
            return self.parse_time(data * 21)
        times = nowtime - lasttime
        self.times_sum += times
        self.times_n += 1
        xx = int(self.times_sum / self.times_n)
        x = self.parse_time(data * xx)
        return x

    def parse_struct_time(self, data):
        return time.strftime('%Y-%m-%d,%H:%M:%S', time.strptime(data, '%y%m%d%H%M%S'))

    def parse_time(self, data):
        data = int(data)
        # d = int(data/3600/24)
        h = str(int(data / 3600))
        m = str(int(data % 3600 / 60))
        s = str(int(data % 3600 % 60))

        return '{}时,{}分,{}秒'.format(h, m, s)

    def wait_recv(self):
        recv = ''
        # for i in range(5):
        data = self.ser.recv()
        #     if data:
        #         recv = '{}{}\n'.format(recv, data)
        #     time.sleep(1)
        # if not recv:
        #     recv = '无接收'
        recv = '[{}], 接收: {}\n'.format(timen(), data)
        print(recv)
        save(recv)
        time.sleep(INTERVAL - 5)


if __name__ == '__main__':
    try:
        m = main()
        m.run()
    except Exception as e:
        print(e)
