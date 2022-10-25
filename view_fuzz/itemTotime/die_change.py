import pandas as pd

'''
axis：默认为 0，表示逢空值剔除整行，如果设置参数 axis＝1 表示逢空值去掉整列。
how：默认为 'any' 如果一行（或一列）里任何一个数据有出现 NA 就去掉整行，如果设置 how='all' 一行（或列）都是 NA 才去掉这整行。
thresh：设置需要多少非空值的数据才可以保留下来的。
subset：设置想要检查的列。如果是多个列，可以使用列名的 list 作为参数。
inplace：如果设置 True，将计算得到的值直接覆盖之前的值并返回 None，修改的是源数据。
'''
path_die = '../dataset/DIE_cov.csv'

# 使用pandas读入
die_comfuzz = pd.read_csv(path_die)  # 读die
die_comfuzz = die_comfuzz.dropna(axis=0, how='all', thresh=None,
                                 subset=["Regions", "Functions", "Lines"], inplace=False)
time_data_die = die_comfuzz
time = [(i + 1) * 2 for i in range(len(time_data_die))]
time_data_die = time_data_die.copy()
time_data_die['time'] = time
# print(time_data_die)
time_data_die.to_csv("../dataset/time_DIE_cov.csv", index=None)
# print("共用了",str(114602/8/60/60)+"个小时")
