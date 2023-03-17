import os


def file_num(start, path, flag):
    for dir in os.listdir(path):  # file 表示的是文件名
        start = start + 1
        if "的副本" in dir:
            flag = flag + 1
            # os.remove(path+"\\"+dir)
        
            print("已删除："+path+"\\"+dir)
    return start,flag


if __name__ == '__main__':
    start = 0
    flag = 0
    path = "C:\\Users\\AidPaike\Desktop\\20221115陕西省档案馆"
    fileNums,flag = file_num(start, path, flag)
    print(fileNums)
    print(flag)
