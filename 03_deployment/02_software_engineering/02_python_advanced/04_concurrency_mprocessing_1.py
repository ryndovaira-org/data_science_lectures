import os
from multiprocessing import Process


def doubler(num):
    """
    Функция умножитель на два
    """
    result = num * 2
    proc_id = os.getpid()
    print('{0} doubled to {1} by process id: {2}'.format(
        num, result, proc_id))


if __name__ == '__main__':
    numbers = [5, 10, 15, 20, 25]
    proc_ids = []

    for index, number in enumerate(numbers):
        proc = Process(target=doubler, args=(number,))
        proc_ids.append(proc)
        proc.start()

    for proc in proc_ids:
        proc.join()
