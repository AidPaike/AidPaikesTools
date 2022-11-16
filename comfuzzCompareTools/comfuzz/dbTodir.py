# sql_config
# # DATABASE_ADDRESS = '127.0.0.1'
# DATABASE_ADDRESS = '10.15.0.26'
# DATABASE_PORT = 8888
# # DATABASE_NAME = 'comfort_cov'
# DATABASE_NAME = 'comfort'
# # DATABASE_NAME = 'comfort_django'
# DATABASE_USER = 'root'
# DATABASE_PASSWORD = 'mysql123'

# !/usr/bin/python
# -*- coding=utf-8 -*-
import time
import threading
import pymysql
import queue
from pymysql.cursors import DictCursor
from dbutils.pooled_db import PooledDB
import numpy as np
import tempfile
import subprocess
import pathlib
import uuid
from tqdm import tqdm,trange

def mysql_connection():
    host = '10.15.0.26'
    user = 'root'
    port = 8888
    password = 'mysql123'
    db = 'comfort'
    charset = 'utf8'
    limit_count = 3  # 最低预启动数据库连接数量
    pool = PooledDB(pymysql, limit_count, maxconnections=15, host=host, user=user, port=port, passwd=password, db=db,
                    charset=charset,
                    use_unicode=True, cursorclass=DictCursor)
    return pool


def saveTojs(testcase_content):
    fileName = str(uuid.uuid1())
    t = time.time()
    fileName += str(round(t))
    testcase_path = dbTosave_path + fileName + ".js"
    try:
        # 此处手动转换为bytes类型再存储是为了防止代码中有乱码而无法存储的情况
        with open(testcase_path, 'w', encoding='utf-8') as f:
            f.write(testcase_content)
    except Exception as e:
        print(e)


def tread_connection_db(id_list):
    start_id = id_list[0]
    end_id = id_list[1]
    con = pool.connection()
    cur = con.cursor()
    sql = '''select id,Testcase_context from Table_Testcase where id>{0} and id<{1}'''.format(start_id, end_id)
    cur.execute(sql)
    # time.sleep(0.5)
    result = cur.fetchall()
    # if result:
    #     print(f"获取到{start_id}---->{end_id}")
    # else:
    #     print('this tread %s result is none' % start_id)
    for i in tqdm(range(len(result)), position=1, desc="saveToJS", leave=False, ncols=180):
        # print(result[i]["Testcase_context"])
        saveTojs(result[i]["Testcase_context"])
    con.close()


def get_db_count():
    print("正在查询数据库中数据量,请稍后...............")
    con = pool.connection()
    cur = con.cursor()
    sql = '''select count(id) from Table_Testcase'''
    cur.execute(sql)
    # time.sleep(0.5)
    result = cur.fetchall()
    # if result:
    #     print(f"获取到{result}条数据")
    # else:
    #     print('查询失败！ 请重试')
    con.close()
    return result


if __name__ == '__main__':
    dbTosave_path = "/root/Comfort_all/data/fzy_testcase/database_testcase/"
    # 创建线程连接池，最大限制15个连接
    pool = mysql_connection()
    # 查询有多少条数据
    get_db_count()
    db_startTime = time.time()
    start = time.time()
    # 创建队列，队列的最大个数及限制线程个数
    q = queue.Queue(maxsize=15)
    # 创建范围列表
    TimeList = np.linspace(200000, 755530, 120, dtype=int)
    range_list = []
    for i in range(len(TimeList)):
        try:
            range_list.append([TimeList[i], TimeList[i + 1]])
        except Exception as e:
            print(e)

    # 测试数据，多线程查询数据库
    for id in tqdm(range(len(range_list)), position=2, desc="rangeList", leave=False, ncols=180):
        # 创建线程并放入队列中
        t = threading.Thread(target=tread_connection_db, args=(range_list[id],))
        q.put(t)
        # 队列队满
        if q.qsize() == 15:
            # 用于记录线程，便于终止线程
            join_thread = []
            # 从对列取出线程并开始线程，直到队列为空
            while not q.empty():
                t = q.get()
                join_thread.append(t)
                t.start()
            # 终止上一次队满时里面的所有线程
            for t in join_thread:
                t.join()
    end = time.time() - start
    print(end)
