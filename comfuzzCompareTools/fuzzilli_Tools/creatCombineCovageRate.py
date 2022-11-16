import subprocess
import os
import tempfile
import pathlib
from typing import List
from tqdm import tqdm
import pandas as pd
import sys


def howManyProfrawCreated(start, path):
    for _ in os.listdir(path):  # file 表示的是文件名
        start = start + 1
    return start


def createCovageRateFile(start, database_len, filename_tmp):
    for i in tqdm(range(start, database_len), position=1, desc="createCoverFile", leave=False, ncols=180):
        testcase_content = testcase_tmp[i]
        timeout = "30"
        # 覆盖率文件路径
        LLVM_PROFILE_FILE = f"/root/fuzzilli/cov_files/profraws/{i + 1}.profraw"
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
                # 获取所有的profraws文件名称,并且替换路径
            except Exception as e:
                print(e)
        cmd_coverage = f"mv {filename_tmp[i]} {filename_tmp[i]}.changed"
        pro = subprocess.Popen(cmd_coverage, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True,
                               stderr=subprocess.PIPE, universal_newlines=True)
        stdout, stderr = pro.communicate()

def get_all_testcase(testcase_path) -> List:
    testcaseAll = []
    for file in os.listdir(testcase_path):  # file 表示的是文件名
        # testcaseAll.append(file)
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
    # print("已储存试验记录")


def init_combine(files):
    file1 = files[0]
    cmd_coverage = f"llvm-profdata-10 merge  -o  1aidpaike.profdata  {file1} && llvm-cov-10 report {COV_ENGHINES_PATH} -instr-profile=1aidpaike.profdata"
    pro = subprocess.Popen(cmd_coverage, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True,
                           stderr=subprocess.PIPE, universal_newlines=True)
    stdout, stderr = pro.communicate()
    # print(stdout)
    # print(stderr)
    # print("初始化文件")
    listAll.append(test_filter(stdout[-175:], 0))
    # print(listAll)
    return listAll


def test_filter(str, flag):
    str_list = str.split()
    str_list.insert(0, flag)
    return str_list


def from_profrawTocsv(files) -> None:
    global flag, listAll
    # 要积攒到多少再存储到csv一次
    for file in tqdm(files, position=2, desc="covTocsv", leave=False, ncols=80):
        flag += 1
        cmd_coverage = f"llvm-profdata-10 merge -sparse {file} 1aidpaike.profdata -o 1aidpaike.profdata && llvm-cov-10 report " \
                       f"{COV_ENGHINES_PATH} -instr-profile=1aidpaike.profdata && rm {file}"
        pro = subprocess.Popen(cmd_coverage, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True,
                               stderr=subprocess.PIPE, universal_newlines=True)
        stdout, stderr = pro.communicate()
        # print(stdout)
        # print(stderr)
        listAll.append(test_filter(stdout[-175:], flag))
    try:
        saveTocsv(listAll)
    except Exception as e:
        print(e)
        print("保存文件出错了")
    listAll = []


def howmanytestall(path):
    cmd = f"ls -lh {path}|wc -l"
    if sys.platform.startswith('win'):  # 假如是windows
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    else:  # 假如是linux
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = p.communicate()
    return int(stdout.decode('ascii'))


def recover_filename(testcase_path):
    print("正在恢复testcases的命名，请稍后.............................")
    recover_testcase_path = filter(recover_filter, os.listdir(testcase_path))
    for file in tqdm(list(recover_testcase_path), position=0, desc="recoverFilename", leave=False, ncols=180):
        cmd_coverage = f"mv {testcase_path + file} {testcase_path + file[:-8]}"
        # print(cmd_coverage)
        pro = subprocess.Popen(cmd_coverage, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True,
                               stderr=subprocess.PIPE, universal_newlines=True)
        stdout, stderr = pro.communicate()
        # print(stdout)
        # print(stderr)


def file_filter(f):
    if f[-3:] in ['.js']:
        return True
    else:
        return False


def recover_filter(f):
    if f[-8:] in ['.changed']:
        return True
    else:
        return False


if __name__ == '__main__':
    print("##########################即将检测已经生成profraws的个数##########################")
    # 求解之前已经处理了多少文件了
    start = 0
    # 生成profraws的文件路径
    create_profraws_path = "/root/fuzzilli/cov_files/profraws/"
    # 插桩后的chakra编译器路径
    COV_ENGHINES_PATH = '/root/.jsvu/engines/chakra-1.13-cov/ch'
    # 生成的testcase存储路径
    testcase_path = "/root/fuzzilli/interesting/"
    # 旗帜：tmp list保存多少个cov数据进行一次写入csv操作
    flag = 0
    # 已经创建了多少profraw了
    created_profraw_len = howmanytestall(create_profraws_path)
    print("目前profraw文件存在：", created_profraw_len)
    print("##########################即将检测testcase的个数##################################")
    # 所有的testcase组成的列表    内存溢出
    # testcaseAll = get_all_testcase(testcase_path)
    print("目前testcase存在：", howmanytestall(testcase_path))
    print("##########################即将开始生成profraw测覆盖率文件,并同时合并写入csv##########################")
    # 即将合并覆盖率并写入csv文件
    listAll = []
    testcase_tmp = []
    filename_tmp = []
    js_testcase_path = filter(file_filter, os.listdir(testcase_path))
    for file in tqdm(list(js_testcase_path), position=3, desc="All", leave=False, ncols=180):  # file 表示的是文件名
        filename = testcase_path + file
        file = open(filename)
        try:
            file_context = file.read()
            testcase_tmp.append(file_context.replace("gc();", ""))
            filename_tmp.append(filename)
        finally:
            file.close()

        if len(testcase_tmp) >= 11:
            createCovageRateFile(0, len(testcase_tmp), filename_tmp=filename_tmp)

        if howmanytestall(create_profraws_path) > 1:
            files = os.listdir(create_profraws_path)
            files = [create_profraws_path + i for i in files]
            # 如果不存在结果csv 则建立这个文件
            if not os.path.exists("testcsv.csv"):
                listAll = init_combine(files)
            # 生成写入csv
            from_profrawTocsv(files)
            testcase_tmp = []
            filename_tmp = []

    # 恢复testcase
    recover_filename(testcase_path)
