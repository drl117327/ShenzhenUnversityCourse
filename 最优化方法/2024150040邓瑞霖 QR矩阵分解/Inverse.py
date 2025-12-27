import scipy.io as sio
import numpy as np
import Gram_Schmidt
def load_data():
    data = sio.loadmat('./MatrixB.mat')
    data = data['B']
    return data

data = load_data()

def is_invertible_det(A, tol=1e-12):
    """通过行列式判断矩阵是否可逆"""
    return abs(np.linalg.det(A)) > tol


def invertible(A):
    if is_invertible_det(A):
        Q, R = Gram_Schmidt.Gram_Schmidt(A)
        A_inv = np.linalg.inv(R) @ Q.T
        return A_inv
    else:
        return None
print("矩阵的逆为:\n", np.linalg.inv(data))
print("矩阵的逆为:\n", invertible(data))