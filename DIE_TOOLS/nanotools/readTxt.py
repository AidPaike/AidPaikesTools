"""
    #file_context是一个string，读取完后，就失去了对test.txt的文件引用
    #file_context=open(file).read().splitlines()，则
    #file_context是一个list，每行文本内容是list中的一个元素
"""
file = open('testdata/testcase.txt')
try:
    file_context = file.read()
    print(file_context)
finally:
    file.close()
