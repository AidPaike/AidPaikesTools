import pandas as pd
import matplotlib.pyplot as plt

path_die = 'dataset/time_DIE_cov.csv'

# 使用pandas读入
data_die = pd.read_csv(path_die)  # 读die
# # 按列分离数据
y_die = data_die[['Cover.1']]  # 读取某一列

y_die = list(y_die["Cover.1"])

x_die = data_die[['time']]

x_die = list(x_die['time'])

_data = [float(str(i).replace("%","")) for i in y_die]

di = x_die

pd.DataFrame({'DIE_cov': _data},index=di).plot(kind='line')

plt.savefig(r'images/die_cov.png', dpi=200)
plt.show()  # 显示当前正在编译的图像
