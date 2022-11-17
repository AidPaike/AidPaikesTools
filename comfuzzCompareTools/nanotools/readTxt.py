"""
    #file_context是一个string，读取完后，就失去了对test.txt的文件引用
    #file_context=open(file).read().splitlines()，则
    #file_context是一个list，每行文本内容是list中的一个元素
"""
import os
from typing import List

file = open('testdata/testcase.txt')
try:
    file_context = file.read()
    print(file_context)
finally:
    file.close()


def get_all_testcase(testcase_path) -> List:
    testcaseAll = []
    for file in os.listdir(testcase_path):  # file 表示的是文件名
        testcaseAll.append(file)
        file = open(testcase_path + file)
        try:
            file_context = file.read()
            testcaseAll.append(file_context)
        finally:
            file.close()
    return testcaseAll
