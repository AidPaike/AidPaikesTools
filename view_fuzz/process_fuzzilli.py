import re
import pandas as pd


def read_log():
    global success_rate_list
    global Coverage_list
    global totalsample_list
    """
    读取日志文件,进行数据重组,写入mysql
    :return:
    """
    file = "./dataset/fuzzilli.log"
    with open(file) as f:
        """使用while循环每次只读取一行,读到最后一行的时候结束"""
        while True:
            lines = f.readline()
            if not lines:
                break
            success_rate = re.match(r'Success Rate:(.*\d)', lines)
            coverage = re.match(r'Coverage:(.*?)%', lines)
            totalsample = re.match(r'Total Samples:(.*?)\n', lines)
            if success_rate:
                # print(success_rate.group(1).replace(" ", ""))
                success_rate_list.append(success_rate.group(1).replace(" ", ""))
            if coverage:
                # print(coverage.group(1).replace(" ", ""))
                Coverage_list.append(coverage.group(1).replace(" ", ""))
            if totalsample:
                # print(totalsample.group(1).replace(" ", ""))
                totalsample_list.append(totalsample.group(1).replace(" ", ""))
        return success_rate_list, Coverage_list, totalsample_list



def Save_to_Csv(data, file_name, Save_format='csv', Save_type='col'):
    # data
    # 输入为一个字典，格式： { '列名称': 数据,....}
    # 列名即为CSV中数据对应的列名， 数据为一个列表

    # file_name 存储文件的名字
    # Save_format 为存储类型， 默认csv格式， 可改为 excel
    # Save_type 存储类型 默认按列存储， 否则按行存储

    # 默认存储在当前路径下

    import pandas as pd
    import numpy as np

    Name = []
    times = 0

    if Save_type == 'col':
        for name, List in data.items():
            Name.append(name)
            if times == 0:
                Data = np.array(List).reshape(-1, 1)
            else:
                Data = np.hstack((Data, np.array(List).reshape(-1, 1)))

            times += 1

        Pd_data = pd.DataFrame(columns=Name, data=Data)

    else:
        for name, List in data.items():
            Name.append(name)
            if times == 0:
                Data = np.array(List)
            else:
                Data = np.vstack((Data, np.array(List)))

            times += 1

        Pd_data = pd.DataFrame(index=Name, data=Data)

    if Save_format == 'csv':
        Pd_data.to_csv('./' + file_name + '.csv', encoding='utf-8')
    else:
        Pd_data.to_excel('./' + file_name + '.xls', encoding='utf-8')

if __name__ == '__main__':
    success_rate_list = []
    Coverage_list = []
    totalsample_list = []
    read_log()
    print(len(success_rate_list))
    print(len(Coverage_list))
    print(len(totalsample_list))
    Data = {'success_rate_list': success_rate_list, 'Coverage_list': Coverage_list, 'totalsample_list': totalsample_list}
    Save_to_Csv(data=Data, file_name='fuzzilli_data', Save_format='csv', Save_type='col')
