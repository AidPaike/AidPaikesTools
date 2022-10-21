import subprocess
import os
import tempfile
import pathlib
from typing import List
from tqdm import tqdm
import pandas as pd


def howManyProfrawCreated(start, path):
    for _ in os.listdir(path):  # file 表示的是文件名
        start = start + 1
    return start


def createCovageRateFile(start, database_len):
    for i in tqdm(range(start, database_len)):
        testcase_content = testcaseAll[i]
        timeout = "30"
        # 覆盖率文件路径
        LLVM_PROFILE_FILE = f"/root/DIE/cov_files/profraws/{i + 1}.profraw"
        my_env = os.environ.copy()
        my_env['LLVM_PROFILE_FILE'] = LLVM_PROFILE_FILE

        with tempfile.NamedTemporaryFile(prefix="javascriptTestcase_", suffix=".js", delete=True) as f:
            testcase_path = pathlib.Path(f.name)

            try:
                # 此处手动转换为bytes类型再存储是为了防止代码中有乱码而无法存储的情况
                testcase_path.write_bytes(bytes(testcase_content, encoding="utf-8"))
                cmd = ["timeout", "-s9", timeout, COV_ENGHINES_PATH, testcase_path]
                pro = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, env=my_env,
                                       stderr=subprocess.PIPE, universal_newlines=True)
                stdout, stderr = pro.communicate()
                # print(stdout)
                # print(cmd_coverage)
                # print(stderr)
            except Exception as e:
                print(e)


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


def saveTocsv(listAll):
    name = ['nums', 'Regions', 'MissedRegions', 'Cover', 'Functions', 'MissedFunctions', 'Executed', 'Lines',
            'MissedLines', 'Cover']
    test = pd.DataFrame(columns=name, data=listAll)
    if not os.path.exists("testcsv.csv"):
        test.to_csv('./testcsv.csv', encoding='gbk', index=None)
    else:
        test.to_csv('./testcsv.csv', encoding='gbk', index=None, mode='a', header=False)
    print("已储存试验记录")


def init_combine(files):
    file1 = files[0]
    cmd_coverage = f"llvm-profdata-10 merge  -o  1aidpaike.profdata  {file1} && llvm-cov-10 report {COV_ENGHINES_PATH} -instr-profile=1aidpaike.profdata"
    pro = subprocess.Popen(cmd_coverage, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True,
                           stderr=subprocess.PIPE, universal_newlines=True)
    stdout, stderr = pro.communicate()
    # print(stdout)
    # print(stderr)
    print("初始化文件")
    listAll.append(test_filter(stdout[-175:], 0))
    print(listAll)
    return listAll


def test_filter(str, flag):
    str_list = str.split()
    str_list.insert(0, flag)
    return str_list


def from_profrawTocsv(files) -> None:
    global flag, listAll
    # 要积攒到多少再存储到csv一次
    range_list = [i * 10 for i in range(100000)]
    for file in tqdm(files):
        flag += 1
        cmd_coverage = f"llvm-profdata-10 merge -sparse {file} 1aidpaike.profdata -o 1aidpaike.profdata && llvm-cov-10 report " \
                       f"{COV_ENGHINES_PATH} -instr-profile=1aidpaike.profdata && rm {file}"
        pro = subprocess.Popen(cmd_coverage, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True,
                               stderr=subprocess.PIPE, universal_newlines=True)
        stdout, stderr = pro.communicate()
        # print(stdout)
        # print(stderr)
        if flag in range_list:
            try:
                saveTocsv(listAll)
            except Exception as e:
                print(e)
                print("保存文件出错了")
            listAll = []
        listAll.append(test_filter(stdout[-175:], flag))


if __name__ == '__main__':
    print("##########################即将检测已经生成profraws的个数##########################")
    # 求解之前已经处理了多少文件了
    start = 0
    # 生成profraws的文件路径
    create_profraws_path = "/root/DIE/cov_files/profraws/"
    # 插桩后的chakra编译器路径
    COV_ENGHINES_PATH = '/root/.jsvu/engines/chakra-1.13-cov/ch'
    # 生成的testcase存储路径
    testcase_path = "/root/DIE/testcase/"
    # 旗帜：tmp list保存多少个cov数据进行一次写入csv操作
    flag = 0
    # 已经创建了多少profraw了，如果中途异常可以避免重新运行
    created_profraw_len = howManyProfrawCreated(start, create_profraws_path)
    print("之前已经完成了生成profraw文件：", created_profraw_len)
    print("##########################即将检测testcase的个数##################################")
    # 所有的testcase组成的列表
    testcaseAll = get_all_testcase(testcase_path)
    # 覆盖率最后生成csv的属性列表
    listAll = []
    # 一共有多少个testcase
    database_len = len(testcaseAll)
    print("目前testcase有这些：", database_len)
    print("##########################即将开始生成profraw测覆盖率文件##########################")
    # 进行测试testcase覆盖率，并生成profraw
    createCovageRateFile(created_profraw_len, database_len)
    # 获取所有的profraws文件名称,并且替换路径
    files = os.listdir(create_profraws_path)
    files = [create_profraws_path + i for i in files]

    # 如果不存在结果csv 则建立这个文件
    if not os.path.exists("DIE-Cov.csv"):
        listAll = init_combine(files)

    # 生成写入csv
    print("##########################即将合并覆盖率并写入csv文件##########################")
    from_profrawTocsv(files)
