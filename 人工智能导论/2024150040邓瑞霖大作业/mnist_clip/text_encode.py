import torch
from torch import nn
import torch.nn.functional as F

class TextEncode(nn.Module):
    def __init__(self):
        super().__init__()
        self.embed = nn.Embedding(num_embeddings=10, embedding_dim=16)
        self.linear1 = nn.Linear(in_features=16, out_features=64)
        self.linear2 = nn.Linear(in_features=64, out_features=16)
        self.wt=nn.Linear(in_features=16,out_features=10)
        self.ln = nn.LayerNorm(10)
    
    def forward(self,x):
        # 通过词嵌入层，输入的x是整数，经过嵌入变成16维
        x=self.embed(x)

        # 第一层全连接层，经过ReLU激活函数
        x=F.relu(self.linear1(x))
        # 第二层全连接层，经过ReLU激活函数
        x=F.relu(self.linear2(x))

        # 经过第三层全连接层，输出8维的向量
        x=self.wt(x)

        # 通过层归一化，规范化输出
        x=self.ln(x)
        return x 
    
if __name__=='__main__':
    text_encoder=TextEncode()
    x=torch.tensor([1, 2, 3, 4, 5, 6, 7, 8, 9, 0])
    y=text_encoder(x)
    print(y.shape)
