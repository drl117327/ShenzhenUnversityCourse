import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt
import pandas as pd
# 设置数值精度阈值
EPSILON = 1e-10

# 加载数据
def load_data():
    data = sio.loadmat('./Matrix_A_b.mat')
    A = data['A']
    b = data['b']
    return A, b # 50 * 50
A, b = load_data()
print(A.shape)
print(b.shape)

def Gram_Schmidt(data):
    m, n = data.shape
    Q = np.zeros((m, n))  
    R = np.zeros((n, n))
    for i in range(n):
        v = data[:, i]
        for j in range(i):
            R[j, i] = np.dot(Q[:, j], v)
            v = v - R[j, i] * Q[:, j]
        # 计算范数并检查是否接近零
        norm_v = np.linalg.norm(v)
        R[i, i] = norm_v
        Q[:, i] = v / R[i, i]
    
    return Q, R


def least_square_solution(A, b):
    Q, R = np.linalg.qr(A)
    Q, R = Gram_Schmidt(A)
    print(Q.shape, R.shape)
    Qt_b = Q.T @ b
    R = np.linalg.inv(R)
    x = R @ Qt_b
    return x

print("最小二乘解为：", least_square_solution(A, b))