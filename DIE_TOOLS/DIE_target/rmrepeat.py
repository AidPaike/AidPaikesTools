#! /usr/bin/python3
'''
通过md5加密结果进行去重
'''
import os
import hashlib
from tqdm import tqdm


def get_md5(file_path):
    if not os.path.isfile(file_path):
        return
    file_hash = hashlib.md5()
    f = open(file_path, 'rb')
    while True:
        b = f.read(8096)
        if not b:
            break
        file_hash.update(b)
    f.close()
    return file_hash.hexdigest()


class Md5Delete(object):
    """
    删除同目录下md5相同的文件。
    """
    def __init__(self, dir_path):
        self.dir_path = dir_path
        self.file_path_md5 = {}

    def check_md5(self):
        dir_path = self.dir_path
        for root, dirs, files in tqdm(os.walk(dir_path)):
            for i in tqdm(range(len(files))):
                file_path = os.path.join(root, files[i])
                file_md5 = get_md5(file_path)
                self.file_path_md5[file_path] = file_md5

    def judge_md5_delete(self):
        length = len(self.file_path_md5)
        i, j = 0, 0
        is_delete = 0
        pbar = tqdm(total=length)
        new_file_path_md5_list = list(self.file_path_md5)
        while True:
            pbar.update(1)
            is_delete = 0
            j = 0
            if i >= length:
                break
            first_file_md5 = self.file_path_md5[new_file_path_md5_list[i]]
            first_file_path = new_file_path_md5_list[i]
            for j in range(length):
                if j >= length:
                    break
                if j <= i:
                    continue
                second_file_md5 = self.file_path_md5[new_file_path_md5_list[j]]
                second_file_path = new_file_path_md5_list[j]

                if first_file_md5 == second_file_md5:
                    self.file_path_md5.pop(second_file_path)
                    # 删除了需要重新生成list
                    new_file_path_md5_list = list(self.file_path_md5)
                    is_delete = 1
                    length = len(self.file_path_md5)
                    os.remove(second_file_path)
                else:
                    j += 1
            if is_delete == 0:
                i += 1
        pbar.close()
        pass

    def run(self):
        self.check_md5()
        self.judge_md5_delete()


def run():
    mmd5 = Md5Delete(r"/DIE/process_data/output_testcase")
    mmd5.run()
    pass


if __name__ == '__main__':
    run()
