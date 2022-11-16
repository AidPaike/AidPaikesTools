from pylab import *

mpl.rcParams['font.sans-serif'] = ['SimHei']  # 添加这条可以让图形显示中文

x_axis_data1 = [i for i in range(10)]
x_axis_data2 = [i + 1 for i in range(10)]
y_axis_data1 = [12, 17, 15, 12, 16, 14, 15, 13, 18, 19]
y_axis_data2 = [1, 4, 2, 6, 4, 2, 1, 6, 4, 2]

plt.plot(x_axis_data1, y_axis_data1)
plt.plot(x_axis_data2, y_axis_data2)
plt.show()
