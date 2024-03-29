import numpy as np
import matplotlib.pyplot as plt
import os

# 指定文件夹路径
folder_path = 'D:/Atomsk/Model/合金拉伸/CoNiCr/Outputs/75_150_600/Rate'

# 初始化多维列表
data_list = np.zeros((1, 5), dtype=int)

def plot_per(data_list):
    data_sum = np.sum(data_list, axis=1)[0]
    data_list = data_list / data_sum
    plt.figure()
    plt.plot(range(data_list.shape[0]), data_list[:, 1])
    plt.plot(range(data_list.shape[0]), data_list[:, 2] + data_list[:, 1])
    plt.plot(range(data_list.shape[0]), data_list[:, 3] + data_list[:, 2] + data_list[:, 1])
    plt.plot(range(data_list.shape[0]), data_list[:, 4] + data_list[:, 3] + data_list[:, 2] + data_list[:, 1])
    plt.plot(range(data_list.shape[0]), data_list[:, 0] + data_list[:, 4] + data_list[:, 3] + data_list[:, 2] + data_list[:, 1])
    plt.legend(["FCC", "HCP", "BCC", "ICO", "Other"])
    plt.xlabel("Steps")
    plt.ylabel("Percentages")
    plt.yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1], ['0', '10', '20', '30', '40', '50', '60', '70', '80', '90', '100'])
    plt.show(block=True)


# 遍历文件夹中的文件
num_file = len(os.listdir(folder_path))
for num in range(num_file):
    filename = 'Rate.' + str(num)
    # 仅处理以 'Rate.' 开头并且后缀为数字的文件
    if filename.startswith('Rate.') and filename.split('.')[1].isdigit():
        # 拼接文件路径
        file_path = os.path.join(folder_path, filename)

        # 打开文件并逐行读取数据
        with open(file_path, 'r') as file:
            # 初始化一个列表用于存储当前文件的数据
            file_data = np.zeros((1, 5),dtype=int)
            index = 0
            # 逐行读取文件内容
            for line in file:
                # 如果行以 # 开头，则是数据行，将其拆分为字段并添加到列表中
                if line[0] != '#':
                    fields = line.strip().split()
                    # 将数据转换为合适的格式，并添加到文件数据列表中
                    file_data[[0], [index]] = fields[1]
                    index += 1
            # 将当前文件的数据列表添加到总的多维列表中
            data_list = np.append(data_list, file_data, axis=0)

# 输出多维列表
data_list = np.delete(data_list, 0, axis=0)
np.savetxt("rate_data.txt", data_list, fmt="%s")

plt.figure()
plt.plot(range(data_list.shape[0]), data_list[:, 0])
plt.plot(range(data_list.shape[0]), data_list[:, 1])
plt.plot(range(data_list.shape[0]), data_list[:, 2])
plt.plot(range(data_list.shape[0]), data_list[:, 3])
plt.plot(range(data_list.shape[0]), data_list[:, 4])
plt.legend([ "Other", "FCC", "HCP", "BCC", "ICO",])

plot_per(data_list)



