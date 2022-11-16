import pandas as pd
import matplotlib.pyplot as plt
from pylab import *
from matplotlib.font_manager import FontProperties

# 支持中文
mpl.rcParams['font.sans-serif'] = ['SimHei']

path_die = 'dataset/time_DIE_cov.csv'
path_comfuzz = 'dataset/time_comfuzz_data_15.csv'
path_codeAl = 'dataset/time_codeAl_data_15.csv'

# 使用pandas读入
data_comfuzz = pd.read_csv(path_comfuzz)  # 读comfuzz
data_die = pd.read_csv(path_die)  # 读die
data_codeAl = pd.read_csv(path_codeAl)  # 读codeAl
# # 按列分离数据
y_die = list(data_die[['Cover.1']]["Cover.1"])  # 读取某一列
x_die = list(data_die[['time']]['time'])

y_comfuzz = list(data_comfuzz[['Cover.1']]["Cover.1"])  # 读取某一列
x_comfuzz = list(data_comfuzz[['time']]['time'])

y_codeAl = list(data_codeAl[['Cover.1']]["Cover.1"])  # 读取某一列
x_codeAl = list(data_codeAl[['time']]['time'])

_data_die = [float(str(i).replace("%", "")) for i in y_die]
_data_comfuzz = [float(str(i).replace("%", "")) for i in y_comfuzz]
_data_codeAl = [float(str(i).replace("%", "")) for i in y_codeAl]


_data_die = [round(i * 50520 * 0.01) for i in _data_die]
_data_comfuzz = [round(i * 50520 * 0.01) for i in _data_comfuzz]
_data_codeAl = [round(i * 50520 * 0.01) for i in _data_codeAl]

# plt.plot(x_axis_data, y_axis_data, 'ro-', color='#4169E1', alpha=0.8, label='一些数字')

plt.plot(x_die, _data_die, label='die')
plt.plot(x_comfuzz, _data_comfuzz, label='comfuzz')
plt.plot(x_codeAl, _data_codeAl, label='CodeAlchemist')


plt.legend(loc="upper right")
plt.xlabel('Time / Second')
plt.ylabel('lines Coverage')
plt.ticklabel_format(style='plain')
plt.savefig(r'images/di&comfuzz&CodeAlchemist.png', dpi=200)
plt.show()  # 显示当前正在编译的图像
