import numpy as np
import matplotlib.pyplot as plt
import scipy.io
from scipy.stats import mode

# ========================== 数据加载 ==========================
def load_data():
    try:
        images_data = scipy.io.loadmat('./train_images.mat')
        labels_data = scipy.io.loadmat('./train_labels.mat')
        train_images = images_data['train_images']   # (28, 28, N)
        train_labels = labels_data['train_labels'].flatten()
        print(f"数据加载完成: 图像数量 {train_images.shape[-1]}, 标签数 {len(train_labels)}")
        return train_images, train_labels
    except Exception as e:
        print(f"数据加载失败: {e}")
        return None, None


# ========================== 手写 PCA ==========================
def pca(X, n_components=2):
    X_mean = np.mean(X, axis=0)
    X_centered = X - X_mean
    cov_matrix = np.cov(X_centered, rowvar=False)
    eig_vals, eig_vecs = np.linalg.eigh(cov_matrix)
    sorted_indices = np.argsort(eig_vals)[::-1]
    top_vectors = eig_vecs[:, sorted_indices[:n_components]]
    X_reduced = np.dot(X_centered, top_vectors)
    return X_reduced


# ========================== K-Means 实现 ==========================
def kmeans(X, k=10, max_iters=100, true_labels=None):
    np.random.seed(42)
    n_samples = X.shape[0]
    indices = np.random.choice(n_samples, k, replace=False)
    centroids = X[indices]

    accuracies = []

    for i in range(1, max_iters + 1):
        # 计算每个样本到质心的距离
        distances = np.linalg.norm(X[:, np.newaxis] - centroids, axis=2)
        cluster_labels = np.argmin(distances, axis=1)

        # 更新质心
        new_centroids = np.array([
            X[cluster_labels == j].mean(axis=0) if np.any(cluster_labels == j)
            else centroids[j]
            for j in range(k)
        ])
        centroids = new_centroids

        # 每10次计算一次准确率
        if true_labels is not None and i % 10 == 0:
            acc = clustering_accuracy(cluster_labels, true_labels)
            accuracies.append((i, acc))
            print(f"迭代 {i} 次准确率: {acc:.4f}")

    return cluster_labels, accuracies, centroids


# ========================== 聚类准确率 ==========================
def clustering_accuracy(pred_labels, true_labels):
    labels = np.zeros_like(pred_labels)
    for i in range(10):
        mask = (pred_labels == i)
        if np.sum(mask) == 0:
            continue
        labels[mask] = mode(true_labels[mask], keepdims=False)[0]
    acc = np.mean(labels == true_labels)
    return acc


# ========================== 主程序 ==========================
if __name__ == "__main__":
    train_images, train_labels = load_data()
    train_images = train_images[:,:,:100]
    train_labels = train_labels[:100]
    print(train_images.shape, train_labels.shape)
    if train_images is None:
        exit()

    n_samples = train_images.shape[-1]
    
    X = train_images.reshape(-1, n_samples).T / 255.0  # (N, 784)

    # ---------- PCA降维到二维 ----------
    print("正在进行PCA降维...")
    X_reduced = pca(X, n_components=2)

    # ---------- 绘制聚类前散点图 ----------
    plt.figure(figsize=(6, 6))
    plt.scatter(X_reduced[:, 0], X_reduced[:, 1], c=train_labels, cmap='tab10', s=10)
    plt.title("True labels")
    plt.xlabel("1")
    plt.ylabel("2")
    plt.colorbar(label="labels")
    plt.show()

    # ---------- 执行K-Means ----------
    print("开始执行K-Means聚类...")
    cluster_labels, accuracies, centroids = kmeans(X_reduced, k=10, max_iters=100, true_labels=train_labels)

    # ---------- 绘制聚类后的二维散点图 ----------
    plt.figure(figsize=(6, 6))
    plt.scatter(X_reduced[:, 0], X_reduced[:, 1], c=cluster_labels, cmap='tab10', s=10)
    plt.title("k-means result")
    plt.xlabel(" 1")
    plt.ylabel(" 2")
    plt.colorbar(label="labels")
    plt.show()

    # ---------- 绘制准确率折线图 ----------
    iters, acc_values = zip(*accuracies)
    plt.figure(figsize=(8, 4))
    plt.plot(iters, acc_values, marker='o', color='b')
    plt.title("accuracy")
    plt.xlabel("step")
    plt.ylabel("accuracy")
    plt.grid(True)
    plt.show()
