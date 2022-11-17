import numpy as np


def spilt_numTorange(start, end, block):
    """
    一个范围的数据分成区间，目的是为了多线程读取数据库，start为20W的原因是comfuzz起初已经处理了20W，从20W开始往后读取即可。总数据量为75W
    :param start:开始索引
    :param end:结束索引
    :param block:分成多少区块
    :return:例表中的元素格式为[start1,start2]，访问时双层索引即可
    """
    start = 200000
    end = 755530
    block = 120
    TimeList = np.linspace(start, end, block, dtype=int)
    range_list = []
    for i in range(len(TimeList)):
        try:
            range_list.append([TimeList[i], TimeList[i + 1]])
        except Exception as e:
            print(e)
    return range_list
