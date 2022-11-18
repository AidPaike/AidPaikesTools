import pandas as pd

path_codeAl = '../dataset/codeAl.csv'

# 使用pandas读入
data_codeAl = pd.read_csv(path_codeAl)  # 读codeAl
data_codeAl = data_codeAl.dropna(axis=0, how='all', thresh=None,
                                 subset=["Regions", "Functions", "Lines"], inplace=False)
time_data_codeAl = data_codeAl[::10]
time = [i+1 for i in range(len(time_data_codeAl))]
time_data_codeAl = time_data_codeAl.copy()
time_data_codeAl['time'] = time
print(time_data_codeAl)
time_data_codeAl.to_csv("../dataset/time_codeAl_data_15.csv",index=None)
#20221118

