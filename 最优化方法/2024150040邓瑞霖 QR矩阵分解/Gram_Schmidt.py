import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt
import pandas as pd
# 设置数值精度阈值
EPSILON = 1e-10

# 加载数据
def load_data():
    data = sio.loadmat('./MatrixA.mat')
    data = data['A']
    return data  # 50 * 50

data = load_data()


# 初始化Q、R矩阵
m, n = data.shape
Q = np.zeros((m, n))  
R = np.zeros((n, n))
# GS算法
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

Q, R = Gram_Schmidt(data)

# 验证Q是否正交，考虑数值误差
def is_orthogonal(Q, tolerance=1e-6):
    QTQ = Q.T @ Q
    I = np.eye(n)
    
    # 将接近零的元素设为精确的零
    QTQ_cleaned = QTQ
    QTQ_cleaned[np.abs(QTQ_cleaned) < tolerance] = 0.0
        
    return np.allclose(QTQ_cleaned, I, atol=tolerance)

print("Q矩阵正交性验证结果:", is_orthogonal(Q))

# 判断Q矩阵是否正交，不考虑数值误差
def is_orthogonal(Q):
    for i in range(n):
        for j in range(i):
            if abs(np.dot(Q[:, i], Q[:, j])) > EPSILON:
                return False
    return True
print("Q矩阵正交性验证结果:", is_orthogonal(Q))

# 验证正交性偏差
k = range(2, n+1)
def orthogonality_bias(Q):
    biases = []
    for i in range(1, n):
        max = 0
        for j in range(i):
            q_i = Q[:, i]
            q_j = Q[:, j]
            temp = abs(np.dot(q_i, q_j))
            if temp > max:
                max = temp
        biases.append(max)
    return biases

biases = orthogonality_bias(Q)



# plt.plot(k, biases, label='Orthogonality Bias')
# plt.xlabel('k')
# plt.ylabel('Orthogonality Bias')
# plt.legend()
# plt.savefig('GS_Orthogonality_Bias.png')
# plt.show()
