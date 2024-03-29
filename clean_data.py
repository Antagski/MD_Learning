import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import pandas as pd

def plot_acf(data):
    # 计算自相关函数
    acf = sm.tsa.acf(data, nlags=100)  # nlags 表示滞后阶数，可以根据需要调整

    # 绘制ACF图表
    plt.figure()
    plt.stem(acf)
    plt.xlabel('Lag')
    plt.ylabel('Autocorrelation')
    plt.title('Autocorrelation Function (ACF)')
    plt.show()


def plot(data):
    plt.figure()
    plt.plot(range(data.shape[0]), data[:, 0])
    plt.grid()
    #plt.xticks(range(0, 800, 2))
    plt.show(block=True)


# 将数据转换为 NumPy 数组
data = np.loadtxt(fname="rate_data.txt", dtype=int)
data = np.delete(data, [0,1,2,4], axis=1)
#plot_acf(data)
plot(data)





