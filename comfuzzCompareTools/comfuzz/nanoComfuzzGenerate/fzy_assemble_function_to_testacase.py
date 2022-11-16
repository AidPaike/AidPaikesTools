# 从Table_Function读取方法，组装用例,再写入Table_Testcase
import time
from multiprocessing.dummy import Pool as ThreadPool
import sys
from pathlib import Path
from tqdm import tqdm
BASE_DIR = str(Path(__file__).resolve().parent.parent)
sys.path.append(BASE_DIR)
from workline.table_to_class.Table_Function_Class import Function_Object
from workline.mysql_tools.Table_Operation import Table_Function


start_time =time.time()
table_Function = Table_Function()

# 获取function表中全部方法
lis = table_Function.selectAllFromTableFunction()
pbar = tqdm(total=len(lis))

def muti_assemble(func):
    function_object = Function_Object(func)
    # print('*' * 25 + f'组装function{function_object.Id}' + '*' * 25)
    function_object.assemble_to_testcase(5)
    pbar.update(1)

pool = ThreadPool()
results = pool.map(muti_assemble, lis)
pool.close()
pool.join()

pbar.close()

end_time =time.time()

print(f'take {int(end_time-start_time)}s')