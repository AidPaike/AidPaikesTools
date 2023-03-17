import os
import shutil


def mymovefile(srcfile, dstpath):  # 移动函数
    if not os.path.isfile(srcfile):
        print("%s not exist!" % (srcfile))
    else:
        fpath, fname = os.path.split(srcfile)  # 分离文件名和路径
        if not os.path.exists(dstpath):
            os.makedirs(dstpath)  # 创建路径
        shutil.move(srcfile, os.path.join(dstpath , fname))  # 移动文件
        print("move %s -> %s" % (srcfile, dstpath + fname))


src_dir = 'C:\\Users\\AidPaike\\Desktop\\20221130雪天'
dst_dir = 'C:\\Users\\AidPaike\\Desktop\\20221130雪天\\JPG'  # 目的路径记得加斜杠

for f in os.listdir(src_dir):
    filename = os.path.join(src_dir,f)
    if f.split(".")[-1] == "JPG":
        mymovefile(filename,dst_dir)
print("done")

