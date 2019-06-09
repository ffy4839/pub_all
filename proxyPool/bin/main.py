from bin.req import *
from bin.func import *

class main():
    def __init__(self):
        self.getProxy = ProxyGet()
        self.checkProxy = ProxyCheck()


    def run(self):
        n = 0
        t_get_start = time.time()
        t_check_start = t_get_start
        while True:
            # t_get = time.time()
            # t_check = t_get
            #
            # if int(t_check-t_check_start) // CHECK_INTERVAL*3600 >= 1:
            #     self.checkProxy.run()
            #
            # if int(t_get)
            self.getProxy.run()
            del_removel_get()

            self.checkProxy.run()
            del_removel_check()

            break

            # time.sleep(10)


if __name__ == '__main__':
    main = main()
    main.run()