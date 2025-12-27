import tkinter as tk
from PIL import Image, ImageDraw
import torch
import torchvision.transforms as transforms
import numpy as np
from clip import CLIP

class CLIPDigitApp:
    def __init__(self, root, model, device):
        self.root = root
        self.root.title("CLIP-based Handwritten Digit Recognition Prototype")
        self.model = model
        model.eval()
        self.device = device
        
        # 初始化画布
        self.canvas_size = 280
        self.canvas = tk.Canvas(root, width=self.canvas_size, height=self.canvas_size, bg="black")
        self.canvas.pack(pady=10)
        
        # 创建一个PIL图像对象用于后台绘图和模型输入
        self.image = Image.new("L", (self.canvas_size, self.canvas_size), 0)
        self.draw = ImageDraw.Draw(self.image)
        
        # 绑定鼠标事件
        self.canvas.bind("<B1-Motion>", self.paint)
        
        # 识别和清除按钮
        self.btn_predict = tk.Button(root, text="recognition", command=self.predict)
        self.btn_predict.pack(side=tk.LEFT, padx=20, pady=10)
        
        self.btn_clear = tk.Button(root, text="clear", command=self.clear_canvas)
        self.btn_clear.pack(side=tk.RIGHT, padx=20, pady=10)
        
        # 结果显示标签
        self.label_result = tk.Label(root, text="recognition result: waiting for input", font=("Helvetica", 20))
        self.label_result.pack(pady=20)

    def paint(self, event):
        # 在画布和PIL图像上同时绘画
        x1, y1 = (event.x - 8), (event.y - 8)
        x2, y2 = (event.x + 8), (event.y + 8)
        self.canvas.create_oval(x1, y1, x2, y2, fill="white", outline="white")
        self.draw.ellipse([x1, y1, x2, y2], fill=255)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("L", (self.canvas_size, self.canvas_size), 0)
        self.draw = ImageDraw.Draw(self.image)
        self.label_result.config(text="recognition result: waiting for input")

    def predict(self):
        # 1. 预处理：将画布图像缩放到 28x28 并标准化
        transform = transforms.Compose([
            transforms.Resize((28, 28)),
            transforms.Grayscale(num_output_channels=1),
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,))
        ])
        img_tensor = transform(self.image).unsqueeze(0).to(self.device)

        # 2. 推理逻辑 (对应文档2中的方法分析)
        with torch.no_grad():
            # 准备文本特征 (0-9)
            text_inputs = torch.arange(10).to(self.device)
            logit = model(img_tensor, text_inputs)
            # 计算相似度 
            prediction = logit.argmax(-1).item()
            confidence = logit[0][prediction].item()

        self.label_result.config(text=f"predict number: {prediction}", font=(50))

# 主程序入口
if __name__ == "__main__":
    # 请确保您已经定义了 CLIP 网络类并加载了权重
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = CLIP().to(device)
    model.load_state_dict(torch.load('model_tmp.pth'))
    
    root = tk.Tk()
    root.geometry("500x400")
    app = CLIPDigitApp(root, model, device)
    root.mainloop()
    pass