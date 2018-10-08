from multiprocessing import *
import time


def s():
    time.sleep(1)
    print('hi!')


class Main():
    def do(self):
        print('hi!')
        time.sleep(1)

    def start(self):
        def a():
            pass

        self.s = Process(target=a)
        self.s.start()


if __name__ == '__main__':
    Main().start()
    Main().start()
