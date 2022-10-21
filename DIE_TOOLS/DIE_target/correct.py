'''
语法正确率
'''
from typing import List
from multiprocessing.dummy import Pool as ThreadPool
import subprocess
import sys
import tempfile
import os
from tqdm import tqdm

os.environ["TOKENIZERS_PARALLELISM"] = "false"

def cmd_jshint(temp_file_path):
    """
    使用jshint对生成的function进行检查\n
    :param temp_file_path: 临时文件位置
    :return: 语法正确返回true,语法错误返回false
    """
    # cmd = ['timeout', '60s', 'jshint', temp_file_path]
    cmd = ['timeout', '10s', 'jshint', '-c', '/DIE/process_data/.jshintrc', temp_file_path]

    if sys.platform.startswith('win'):  # 假如是windows
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    else:  # 假如是linux
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if stdout:
        print(stdout)
    # if stderr:
    #     print("error")
    #     print(stderr)

    if stdout.__len__() > 0:
        jshint_flag = False
    else:  # 通过了检查，此时 test_file_name中就是美化后的代码
        jshint_flag = True
        # print(f"{temp_file_path}right!")
    return jshint_flag


def testJshintPassRate(function):
    global testJshintPassRateSet
    with tempfile.NamedTemporaryFile(delete=True) as tmpfile:
        temp_file_path = tmpfile.name
        # print(temp_file_name)  # /tmp/tmp73zl8gmn
        fine_code = function
        # fine_code = 'var NISLFuzzingFunc = ' + function
        # fine_code = function

        tmpfile.write(fine_code.encode())
        tmpfile.seek(0)
        # tmpTxt = tmpfile.read().decode()
        # print(tmpTxt)
        # 美化函数
        result = cmd_jshint(temp_file_path)
        if result:
            testJshintPassRateSet.add(function)


def repetitionRateGeneratedDataItself(allFunctions):
    noRepeatFunctions = set(allFunctions)
    noRepeatFunctionsSize = len(noRepeatFunctions)
    return noRepeatFunctionsSize


def generateDataWithRepetitionRateTrainingSet(function):
    trainDataFile = '/DIE/process_data/train_data_bos.txt'
    with open(trainDataFile, 'r') as f:
        trainDatasetContents = f.read()
        if function in trainDatasetContents:
            global generateDataWithRepetitionRateTrainingSetCount
            generateDataWithRepetitionRateTrainingSetCount += 1


def averageNumberRowsToGenerateData(function):
    global averageNumberRowsToGenerateDataCount
    averageNumberRowsToGenerateDataCount += len(function.splitlines())


def multithreadedAnalysis(function):
    testJshintPassRate(function)
    # generateDataWithRepetitionRateTrainingSet(function)


def get_allfunctions() -> List:
    functions = []
    path = "/DIE/process_data/output_testcase/"
    count = 0
    for file in tqdm(os.listdir(path)):  # file 表示的是文件名
        count = count + 1
        file = open(path+file)
        try:
            file_context = file.read()
            functions.append(file_context)
        finally:
            file.close()
    print("共获取到了"+str(count)+"个函数文件！")
    return functions


allFunctions = get_allfunctions()

totalSize = len(allFunctions)

print('总共有{}个方法'.format(totalSize))

generateDataWithRepetitionRateTrainingSetCount = 0

testJshintPassRateSet = set()

averageNumberRowsToGenerateDataCount = 0

pool = ThreadPool()

pool.map(multithreadedAnalysis, allFunctions)

pool.close()

pool.join()

# noRepeatFunctionsSize = repetitionRateGeneratedDataItself(allFunctions)

print("生成的用例语法正确率为{:.2%},".format(len(testJshintPassRateSet) / totalSize))

# print("生成数据本身的重复率为{:.2%}".format(1 - noRepeatFunctionsSize / totalSize))

# print("生成数据与训练集的重复率为{:.2%}".format(generateDataWithRepetitionRateTrainingSetCount / totalSize))

# 统计通过语法检查的代码行数
for testJshintPassRate in tqdm(testJshintPassRateSet):
    averageNumberRowsToGenerateData(testJshintPassRate)

print("语法正确方法的平均行数为{}行".format(int(averageNumberRowsToGenerateDataCount / totalSize)))
