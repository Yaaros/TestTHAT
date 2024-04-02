import csv
import os
import torch
import torch.utils.data as Data
from tqdm import tqdm

'''csv文件:7200rows,90000columns'''

def average_list(d_list):
    sum = [0.0 for _ in range(len(d_list[0]))]
    for j in range(len(d_list[0])):
        for i in range(len(d_list)):
            sum[j] += d_list[i][j]
        sum[j] /= len(d_list)
    return sum

'''他这个函数意思是按照时间戳遍历每行数据，然后把

这条疑似并不是关键问题：错误的数据中的temp_list都超级长，这东西根本不是最后一个间隔的东西
因此只使得new_data的长度+1了

'''
def merge_timestamp(data, time_stamp):
    intervel = (time_stamp[len(time_stamp)-1] - time_stamp[0]) / 2000
    cur_range = time_stamp[0] + intervel
    temp_list = []
    new_data = []
    for i in range(len(time_stamp)):
        if time_stamp[i] > cur_range:
            '''第一个数据：先进行依次else再进行3次if，导致在for循环结束时长度为4
            正确的数据是基本全做if分支操作'''
            if len(temp_list) != 0:
                # print(f"我做了if操作，添加了长为{len(average_list(temp_list))}的数据")
                new_data.append(average_list(temp_list))
            else:
                # print(f"我做了else操作，添加了长为{len(data[i])}的数据")
                new_data.append(data[i])
            temp_list = []
            cur_range = cur_range + intervel
        temp_list.append(data[i])
    # print(f"len(new_data) = {len(new_data)}")  # 在这句之前就有问题了
    if len(temp_list) != 0:
        new_data.append(average_list(temp_list))
    if len(new_data) < 2000:
        new_data.append(data[len(time_stamp)-1])
        print("\n!!!!")
    print(len(new_data))
    return new_data[:2000]
    # print("\n")
    # print(f"len(time_stamp): {len(time_stamp)}")
    # print(f"time_Stamp[0]: {time_stamp[0]}")
    # print(f"time_Stamp[len-1]: {time_stamp[len(time_stamp)-1]}")
    # print(f"len(temp_list): {len(temp_list)}")
    # print(f"len(temp_list[0]): {len(temp_list[0])}")
    # print(f"len(new_data): {len(new_data)}")
    # import pdb  # 断点调试
    # pdb.set_trace()


def load_data(root):
    root = root + '\\'
    file_list = os.listdir(root)
    label = []
    data = []
    aclist = ['bed', 'fall', 'pickup', 'run', 'sitdown', 'standup', 'walk']
    #minsize = 15813
    try:
        for file in tqdm(file_list):
            with open(root + file, encoding='utf-8') as f:
                reader = csv.reader(f)
                record = []
                time_stamp = []
                for r in reader:
                    record.append([float(str_d) for str_d in r[1:91]])
                    time_stamp.append(float(r[0]))
                record = merge_timestamp(record, time_stamp)
                float_data = torch.tensor(record, dtype=torch.float32, requires_grad=False)
                data.append(float_data.unsqueeze(0))
                for j in range(len(aclist)):
                    if file.find(aclist[j]) != -1:
                        label.append(j)
                        break
        # import pdb # 断点调试
        # pdb.set_trace()
        data = torch.cat(data, dim=0)
        label = torch.tensor(label)
        data = Data.TensorDataset(data, label)
        torch.save(data, "Data.pt")
        return data
    except Exception as e:
        print(e)

load_data("Data")
