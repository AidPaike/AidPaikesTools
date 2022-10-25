import pandas as pd
import matplotlib.pyplot as plt

path_fuzzilli = './dataset/fuzzilli_data.csv'
path_comfuzz = './dataset/testcsv.csv'
path_die = '../dataset/DIE_cov.csv'

# 使用pandas读入
data_fuzzilli = pd.read_csv(path_fuzzilli)  # 读fuzzilli
data_comfuzz = pd.read_csv(path_comfuzz)  # 读comfuzz
data_die = pd.read_csv(path_die)  # 读die
# # 按列分离数据
# x = data[['ImageID', 'label']]#读取某两列
# print(x)
y_fuzzilli = data_fuzzilli[['Coverage_list']]  # 读取某一列
y_comfuzz = data_comfuzz[['Cover']]  # 读取某一列
y_die = data_die[['Coverage_list']]  # 读取某一列
y_fuzzilli = list(y_fuzzilli["Coverage_list"])
y_comfuzz = list(y_comfuzz["Cover"])
y_die = list(y_die["Cover"])
print(len(y_comfuzz))
print(len(y_fuzzilli))
print(len(y_die))

_dates = [i for i in range(len(y_fuzzilli))]
_data1 = y_fuzzilli
# _data2 = y_comfuzz
# _data2 = [float(str(i).replace("%","")) for i in _data2]
di = pd.DatetimeIndex(_dates, freq=None)

pd.DataFrame({'fuzzilli_cov': _data1},
             index=di).plot.line()  # 图形横坐标默认为数据索引index。
#
plt.savefig(r'images/p1.png', dpi=200)
plt.show()  # 显示当前正在编译的图像

# pd.DataFrame({'fuzzilli_cov': _data1, 'y_comfuzz_cov': _data2},
#              index=di).plot.line()  # 图形横坐标默认为数据索引index。
#
# plt.savefig(r'dataset/p2.png', dpi=200)
# plt.show()  # 显示当前正在编译的图像
