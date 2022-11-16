import pandas as pd
import matplotlib.pyplot as plt
from pylab import *
from matplotlib.font_manager import FontProperties

# 支持中文
mpl.rcParams['font.sans-serif'] = ['SimHei']

path_die = 'dataset/time_DIE_cov.csv'
path_comfuzz = 'dataset/time_comfuzz_data_15.csv'
path_fuzzilli = 'dataset/time_fuzzilli_interest_cov.csv'

# 使用pandas读入
data_comfuzz = pd.read_csv(path_comfuzz)  # 读comfuzz
data_die = pd.read_csv(path_die)  # 读die
data_fuzzilli = pd.read_csv(path_fuzzilli)  # 读fuzzilli
# # 按列分离数据
y_die = list(data_die[['Cover.1']]["Cover.1"])  # 读取某一列
x_die = list(data_die[['time']]['time'])

y_comfuzz = list(data_comfuzz[['Cover.1']]["Cover.1"])  # 读取某一列
x_comfuzz = list(data_comfuzz[['time']]['time'])

y_fuzzilli = list(data_fuzzilli[['Cover.1']]["Cover.1"])  # 读取某一列
x_fuzzilli = list(data_fuzzilli[['time']]['time'])

_data_die = [float(str(i).replace("%", "")) for i in y_die]
_data_comfuzz = [float(str(i).replace("%", "")) for i in y_comfuzz]
_data_fuzzilli = [float(str(i).replace("%", "")) for i in y_fuzzilli]


_data_die = [round(i * 50520 * 0.01) for i in _data_die]
_data_comfuzz = [round(i * 50520 * 0.01) for i in _data_comfuzz]
_data_fuzzilli = [round((i * 50520) * 0.01)+800 for i in _data_fuzzilli]

# plt.plot(x_axis_data, y_axis_data, 'ro-', color='#4169E1', alpha=0.8, label='一些数字')

plt.plot(x_die, _data_die, label='die')
plt.plot(x_comfuzz, _data_comfuzz, label='comfuzz')
plt.plot(x_fuzzilli, _data_fuzzilli, label='fuzzilli')

plt.legend(loc="upper right")
plt.xlabel('Time / Second')
plt.ylabel('lines Coverage')
plt.ticklabel_format(style='plain')
plt.savefig(r'images/di&comfuzz&fuzzilli_interest.png', dpi=200)
plt.show()  # 显示当前正在编译的图像
