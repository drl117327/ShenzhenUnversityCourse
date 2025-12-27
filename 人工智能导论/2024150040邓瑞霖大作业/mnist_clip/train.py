import torch
from dataset import MNIST
from clip import CLIP
import torch.nn.functional as F
from torch.utils.data import DataLoader
import os
import matplotlib.pyplot as plt

DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
EPOCHS = 1000
BATCH_SIZE = 128
COUNT = 10
LR = 1e-5
SAVE_INTERVAL = 1000
NUM_WORKERS = 0  
dataset = MNIST()
# 数据加载器
dataloader = DataLoader(dataset,
                        batch_size=BATCH_SIZE,
                        shuffle=True,
                        num_workers=NUM_WORKERS,
                        persistent_workers=False) 

model = CLIP().to(DEVICE)
model.load_state_dict(torch.load('model_tmp.pth'))
model.train()
optimizer = torch.optim.Adam(model.parameters(), lr=LR)
# 用于记录损失
los = []
x = []

# 迭代寻来你
for epoch in range(EPOCHS + 1):
    while True:
        imgs, labels = next(iter(dataloader))
        if torch.unique(labels).shape[0] < COUNT:
            continue
        target = set()
        indexes = []
        for j in range(BATCH_SIZE):
            if labels[j].item() in target:
                continue
            target.add(labels[j].item())
            indexes.append(j)
            if len(target) == COUNT:
                break
        imgs = imgs[indexes]
        labels = labels[indexes]
        break

    logits = model(imgs.to(DEVICE), labels.to(DEVICE))

    targets = torch.arange(0, COUNT, device=DEVICE)
    # loss
    loss_i = F.cross_entropy(logits, targets)
    loss_t = F.cross_entropy(logits.permute(1, 0), targets)
    loss = (loss_i + loss_t) / 2
    # 前向回代
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    if epoch % 100 == 0:
        print(f"iter: {epoch}, loss: {loss.item():.6f}")
        torch.save(model.state_dict(), "model_tmp.pth")
        os.replace("model_tmp.pth", "model_tmp.pth")

        # 保存损失值
        los.append(loss.item())
        x.append(epoch)

        # 保存损失曲线图
        plt.plot(x, los, label='Loss', color='r')
        plt.xlabel('Iterations')
        plt.ylabel('Loss')
        plt.title('Training Loss Curve')
        plt.legend()
        plt.savefig('loss.png')
        plt.close()  