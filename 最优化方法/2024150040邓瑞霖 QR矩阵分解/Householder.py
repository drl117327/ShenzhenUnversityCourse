import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt
import pandas as pd

def load_data():
    data = sio.loadmat('./MatrixA.mat')
    data = data['A']
    return data
data = load_data()
m, n = data.shape
Q = np.zeros((m, m))
R = np.zeros((m, n))

def householder(data):
    data = data.astype(float)
    R = data.copy()
    Q = np.eye(m)
    for k in range(n):
        # 取出当前列向量
        x = data[k:, k]
        # 构造Householder向量
        e = np.zeros_like(x)
        e[0] = 1.0
        # 计算反射向量
        v = x + np.sign(x[0]) * np.linalg.norm(x) * e
        v = v / np.linalg.norm(v)
        # 构造H_k
        H_k = np.eye(m)
        H_k[k:, k:] -= 2.0 * np.outer(v, v)
        # 更新R和Q
        R = H_k @ R
        Q = Q @ H_k.T
    return Q, R

Q, R = householder(data)
# 验证QR分解的正确性
print("QR分解验证结果:", np.allclose(Q @ R, data))
print("Q 是否正交？ ", np.allclose(Q.T @ Q, np.eye(Q.shape[1])))

# 验证正交性偏差
k = range(2, m+1)
def orthogonality_bias(Q):
    biases = []
    for i in range(1, m):
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

# 绘制正交性偏差图像
plt.plot(k, biases, label='Orthogonality Bias')
plt.xlabel('k')
plt.ylabel('Orthogonality Bias')
plt.legend()
plt.savefig('Householder_Orthogonality_Bias.png')
plt.show()