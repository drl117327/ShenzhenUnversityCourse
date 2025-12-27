import torch 
from torch import nn
from image_encode import ImageEncode
from text_encode import TextEncode

class CLIP(nn.Module):
    def __init__(self, ):
        super().__init__()
        self.img_enc = ImageEncode()
        self.text_enc = TextEncode()
    
    def forward(self, img_x, text_x):
        img_emb = self.img_enc(img_x)
        text_emb = self.text_enc(text_x)
        return img_emb @ text_emb.T
    
    