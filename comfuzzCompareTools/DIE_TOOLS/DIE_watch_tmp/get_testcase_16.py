import os
import time
from shutil import copyfile
from tqdm import trange

for i in trange(10000):
    path_testcase = "/DIE/output_testcase"
    for j in range(16):
        path = path_testcase+"/{}_{}".format(i,j)+".js"
        from_path = "output-"+str(j)+"/.cur_input.js"
        copyfile(from_path,path)
        print("复制"+from_path+"到"+str(path))
    time.sleep(5)
