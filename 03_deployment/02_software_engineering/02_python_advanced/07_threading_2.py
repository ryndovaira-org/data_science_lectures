# модуль thread устарел в Python 3 и переименован в модуль _thread для обратной совместимости
import datetime
from random import randint
import logging
import time

# модуль threading предоставляет богатые возможности и большую поддержку потоков, чем устаревший модуль thread
import threading


class MyThread(threading.Thread):
    def __init__(self, name, counter):
        threading.Thread.__init__(self)
        self.threadID = counter
        self.name = name
        self.counter = counter

    def run(self):
        logging.info("Thread %s: starting", self.counter)
        print_date_and_sleep(self.name, self.counter)
        logging.info("Thread %s: finishing", self.counter)


def print_date_and_sleep(thread_name, counter):
    date_fields = []
    today = datetime.date.today()
    time.sleep(randint(3, 10))
    date_fields.append(today)
    logging.info("%s[%d]: %s" % (thread_name, counter, date_fields[0]))


if __name__ == "__main__":
    dt_format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=dt_format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    logging.info("Main: before creating threads")

    thread_num = 5
    threads = []
    # Создать треды
    for n in range(thread_num):
        threads.append(MyThread(f"Thread", n))
    # thread1 = MyThread("Thread", 1)
    # thread2 = MyThread("Thread", 2)

    logging.info("Main: before running thread")
    # Запустить треды
    for t in threads:
        t.start()
    # thread1.start()
    # thread2.start()

    logging.info("Main: wait for the thread to finish")
    for t in threads:
        t.join()
        pass
    # thread1.join()
    # thread2.join()

    logging.info("Main: all done")
