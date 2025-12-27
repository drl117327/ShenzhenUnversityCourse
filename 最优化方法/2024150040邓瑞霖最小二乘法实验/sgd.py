import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt
import time
def load_data():
    data = sio.loadmat('./Matrix_A_b.mat')
    A = data['A']
    b = data['b']
    return A, b


epochs = 50

def least_square_solution(A, b):
    start = time.time()
    Q, R = np.linalg.qr(A)
    print(Q.shape, R.shape)
    Qt_b = Q.T @ b
    R = np.linalg.inv(R)
    x = R @ Qt_b
    end = time.time()
    print(f"Least square solution time: {end - start} seconds")
    return x

ep = []
def sgd(A, b):
    target = []
    temp = []
    m, n = A.shape
    x_least = least_square_solution(A, b)
    x = np.zeros((n, 1))
    op=0
    start_time = time.time()

    for epoch in range(epochs):
        gradient = A.T @ (A @ x - b)
        lr = np.linalg.norm(gradient) ** 2 / np.linalg.norm(A @ gradient) ** 2
        y = x - lr * gradient
        # 相似程度
        relative_error = np.linalg.norm(y - x_least) / np.linalg.norm(x_least)
        temp.append(relative_error)
        if(np.linalg.norm(x-y) / np.linalg.norm(x)<0.01):
            op=1
        x = y
        target.append(np.linalg.norm(A @ x - b))
        ep.append(epoch + 1)
        # 是否设置最小梯度阈值
        if op==1:
            print(epoch+1)
            break
    end_time = time.time()
    return target, temp, end_time - start_time
target, temp, duration = sgd(*load_data())

plt.plot(ep, temp, color='blue')
plt.xlabel('Epochs')
plt.ylabel('Relative Error')
plt.title('Relative Error decreases with the number of iterations')
plt.legend()
plt.savefig('lr_Relative_Error_30.png')
plt.show()