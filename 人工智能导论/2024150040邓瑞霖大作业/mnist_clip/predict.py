import torch
from dataset import MNIST
from clip import CLIP
import torch.nn.functional as F
from torch.utils.data import DataLoader
import numpy as np
import random

DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
BATCH_SIZE = 128
NUM_WORKERS = 0

# 加载数据
dataset = MNIST(is_train=False)
print(f"MNIST预测数据集大小: {len(dataset)}")

# 创建模型
model = CLIP()
model.load_state_dict(torch.load('model_tmp.pth'))
model.to(DEVICE)
model.eval()

dataloader = DataLoader(
    dataset, 
    batch_size=BATCH_SIZE, 
    shuffle=False,  
    num_workers=NUM_WORKERS
)

text_inputs = torch.arange(0, 10).to(DEVICE)  # 形状: [10]

# 预测
correct = 0
total = 0

with torch.no_grad():
    for batch_idx, (images, labels) in enumerate(dataloader):
        images = images.to(DEVICE)
        labels = labels.to(DEVICE)
        
        # 获取文本特征（提前计算一次即可）
        # 这里需要根据您的CLIP实现调整
        text_features = model.text_enc(text_inputs)  # 假设有这个方法
        text_features = F.normalize(text_features, dim=-1)
        
        # 获取图像特征
        image_features = model.img_enc(images)  # 假设有这个方法
        image_features = F.normalize(image_features, dim=-1)
        
        # 计算相似度（余弦相似度）
        # 形状: [batch_size, 10]
        similarity = image_features @ text_features.T
        
        # 获取预测（相似度最高的类别）
        predictions = similarity.argmax(dim=1)
        
        # 统计
        correct += (predictions == labels).sum().item()
        total += labels.size(0)
        
        # 打印进度
        if (batch_idx + 1) % 10 == 0:
            print(f'已处理: [{batch_idx+1}/{len(dataloader)}] 个批次')

# 输出结果
accuracy = correct / total
print(f'\n总样本数: {total}')
print(f'正确预测: {correct}')
print(f'准确率: {accuracy:.4f} ({accuracy*100:.2f}%)')