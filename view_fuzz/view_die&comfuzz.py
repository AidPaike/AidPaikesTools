import pandas as pd
import matplotlib.pyplot as plt
from pylab import *
from matplotlib.font_manager import FontProperties

# 支持中文
mpl.rcParams['font.sans-serif'] = ['SimHei']

path_die = 'dataset/time_DIE_cov.csv'
path_comfuzz = 'dataset/time_comfuzz_data_15.csv'

# 使用pandas读入
data_comfuzz = pd.read_csv(path_comfuzz)  # 读comfuzz
data_die = pd.read_csv(path_die)  # 读die
# # 按列分离数据
y_die = list(data_die[['Cover.1']]["Cover.1"])  # 读取某一列
x_die = list(data_die[['time']]['time'])

y_comfuzz = list(data_comfuzz[['Cover.1']]["Cover.1"])  # 读取某一列
x_comfuzz = list(data_comfuzz[['time']]['time'])

_data_die = [float(str(i).replace("%", "")) for i in y_die][:len(x_comfuzz)]
_data_comfuzz = [float(str(i).replace("%", "")) for i in y_comfuzz]

di = x_comfuzz

_data_die = [round(i * 90681 * 0.01) for i in _data_die]
_data_comfuzz = [round(i * 90681 * 0.01) for i in _data_comfuzz]


pd.DataFrame({'die': _data_die, 'comfuzz': _data_comfuzz},
             index=di).plot.line()  # 图形横坐标默认为数据索引index。
plt.xlabel('Time / Second')
plt.ylabel('lines Coverage')
plt.ticklabel_format(style='plain')
plt.savefig(r'dataset/di&comfuzz.png', dpi=200)
plt.show()  # 显示当前正在编译的图像
