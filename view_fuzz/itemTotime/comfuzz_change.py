import pandas as pd

path_comfuzz = '../dataset/testcsv.csv'

# 使用pandas读入
data_comfuzz = pd.read_csv(path_comfuzz)  # 读comfuzz
data_comfuzz = data_comfuzz.dropna(axis=0, how='all', thresh=None,
                                 subset=["Regions", "Functions", "Lines"], inplace=False)
time_data_comfuzz = data_comfuzz[::15]
time = [i+1 for i in range(len(time_data_comfuzz))]
time_data_comfuzz = time_data_comfuzz.copy()
time_data_comfuzz['time'] = time
print(time_data_comfuzz)
time_data_comfuzz.to_csv("../dataset/time_comfuzz_data_15.csv",index=None)
# print("共用了",str(114602/8/60/60)+"个小时")

