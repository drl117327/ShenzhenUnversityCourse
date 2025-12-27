from dataset import MNIST
import matplotlib.pyplot as plt 
import torch 
from clip import CLIP
import torch.nn.functional as F
import random

DEVICE='cuda' if torch.cuda.is_available() else 'cpu'   # 设备

dataset=MNIST() # 数据集

model=CLIP().to(DEVICE) # 模型
model.load_state_dict(torch.load('model_tmp.pth'))
model.eval()    # 预测模式
'''
对图片分类
'''
image,label=dataset[0]
print('正确分类:',label)
print(image.shape)
print(image)
exit()

plt.imshow(image.permute(1,2,0))
plt.show()

targets=torch.arange(0,10)  #10种分类
logits=model(image.unsqueeze(0).to(DEVICE),targets.to(DEVICE)) # 1张图片 vs 10种分类
print(logits)
print('CLIP分类:',logits.argmax(-1).item())


"""
随机分类展示
"""
plt.figure(figsize=(20, 10))
for _ in range(10):
    plt.subplot(2, 5, _ + 1)
    index = random.randint(0, len(dataset))
    img, label = dataset[index]
    logits = model(img.unsqueeze(0).to(DEVICE), torch.arange(0, 10).to(DEVICE))
    pre_label = logits.argmax(-1).item()
    plt.imshow(img.permute(1, 2, 0))
    plt.title(f'True: {label}, Pred: {pre_label}', fontsize=20)
    plt.axis('off')
plt.savefig('random_classification.png')
plt.show()