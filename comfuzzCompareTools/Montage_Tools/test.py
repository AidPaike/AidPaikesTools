import numpy as np


TimeList = np.linspace(200000, 755530, 120, dtype=int)
range_list = []
for i in range(len(TimeList)):
    try:
        range_list.append([TimeList[i], TimeList[i + 1]])
    except Exception as e:
        print(e)
