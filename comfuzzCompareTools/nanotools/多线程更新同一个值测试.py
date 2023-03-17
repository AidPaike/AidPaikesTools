from multiprocessing.dummy import Pool as ThreadPool


class threadNum:
    def __init__(self):
        self.public_num = 0

    def add(self):
        self.public_num += 1

    def subtraction(self):
        self.public_num -= 1

    def main(self, function):
        print(str(function), "*****")
        self.add()
        self.subtraction()


if __name__ == '__main__':
    threadNum = threadNum()
    pool = ThreadPool()
    numList = [1, 2, 3]
    pool.map(threadNum.main, numList)
    pool.close()
    pool.join()
    print(threadNum.public_num)
