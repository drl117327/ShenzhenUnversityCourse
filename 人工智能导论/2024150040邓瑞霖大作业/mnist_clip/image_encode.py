import torch
from torch import nn
from torch.nn import functional as F

class Residual(nn.Module):
    def __init__(self, in_channels, out_channels, use_1x1conv=False, strides=1):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=3, 
                              padding=1, stride=strides, bias=False)
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3, 
                              padding=1, bias=False)
        
        if use_1x1conv:
            self.conv3 = nn.Conv2d(in_channels, out_channels, kernel_size=1, 
                                  stride=strides, bias=False)
        else:
            self.conv3 = None
            
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.bn2 = nn.BatchNorm2d(out_channels)
        self.dropout = nn.Dropout2d(0.1)  # 添加dropout
        
    def forward(self, X):
        Y = F.relu(self.bn1(self.conv1(X)))
        Y = self.dropout(Y)  # dropout
        Y = self.bn2(self.conv2(Y))
        
        if self.conv3:
            X = self.conv3(X)
            
        return F.relu(X + Y)


class ImageEncode(nn.Module):
    """改进的ResNet编码器"""
    def __init__(self, dropout_rate=0.5):
        super().__init__()
        
        # 初始层
        self.initial = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=3, stride=1, padding=1, bias=False),  # 28x28
            nn.BatchNorm2d(16),
            nn.ReLU(),
        )
        # 更轻量的ResNet块
        # 通道数: 16 -> 32 -> 64 -> 128
        self.layer1 = self._make_layer(16, 32, 2, stride=1)  # 第一个块不降采样
        self.layer2 = self._make_layer(32, 64, 2, stride=2)  # 14x14
        self.layer3 = self._make_layer(64, 128, 2, stride=2)  # 7x7
        
        # 全局平均池化
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        # 分类头 - 改进
        self.classifier = nn.Sequential(
            nn.Dropout(dropout_rate),
            nn.Linear(128, 64),
            nn.BatchNorm1d(64),  # 添加BatchNorm
            nn.ReLU(),
            nn.Dropout(dropout_rate/2),
            nn.Linear(64, 10)
        )
        
        
    def _make_layer(self, in_channels, out_channels, num_blocks, stride):
        layers = []
        
        # 第一个块可能改变尺寸
        layers.append(Residual(in_channels, out_channels, 
                             use_1x1conv=(in_channels != out_channels or stride != 1),
                             strides=stride))
        
        # 后续块
        for _ in range(1, num_blocks):
            layers.append(Residual(out_channels, out_channels))
            
        return nn.Sequential(*layers)
    
    
    def forward(self, x):
        x = self.initial(x)
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x