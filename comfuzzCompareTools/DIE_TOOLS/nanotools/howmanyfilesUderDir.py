import os
path = "/root/Comfort_all/data/cov_files/profraws_all"
count = 0
for file in os.listdir(path):  # file 表示的是文件名
    count = count + 1
print(count)
