# labs/03_dl_overfitting.py
# 对应第五章：深度学习训练（过拟合与早停机制观测）
# 目标：构建一个故意产生过拟合的网络，并观测其训练集与验证集的 Loss 曲线分离(剪刀差)。

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

def run_experiment():
    print("--- 深度学习实战：过拟合可观测证据 ---\n")
    
    # 1. 制造极少量、且带噪音的数据 (故意制造过拟合倾向)
    torch.manual_seed(42)
    X = torch.rand(50, 10)  # 仅 50 条样本，每条 10 个特征
    y = (X.sum(dim=1) > 5).float().view(-1, 1) # 简单规则生成的二分类标签
    
    # 将一部分数据人为变为干扰噪音
    y[:10] = 1 - y[:10]
    
    # 强行切分：前 40 条训练，后 10 条验证
    X_train, y_train = X[:40], y[:40]
    X_val, y_val = X[40:], y[40:]
    
    # 2. 构建一个“用力过度”的庞大神经网络
    # 对于简单的 50 个样本而言，3个隐藏层共计几百个神经元，极易产生“死记硬背”
    model = nn.Sequential(
        nn.Linear(10, 64), nn.ReLU(),
        nn.Linear(64, 64), nn.ReLU(),
        nn.Linear(64, 1), nn.Sigmoid()
    )
    
    criterion = nn.BCELoss() # 二分类交叉熵
    optimizer = optim.Adam(model.parameters(), lr=0.01)
    
    print("模型构建完毕，开始训练（无早停机制）...\n")
    
    # 3. 记录日志，观察 Loss 变化
    epochs = 100
    for epoch in range(1, epochs + 1):
        model.train()
        optimizer.zero_grad()
        out_train = model(X_train)
        loss_train = criterion(out_train, y_train)
        loss_train.backward()
        optimizer.step()
        
        # 验证阶段 (不更新梯度)
        model.eval()
        with torch.no_grad():
            out_val = model(X_val)
            loss_val = criterion(out_val, y_val)
            
        # 观测现象：大概在 20~30 epoch 之后，train loss 继续向 0 逼近，
        # 而 val loss 开始反弹上升 —— 这就是典型的“过拟合”铁证。
        if epoch % 20 == 0 or epoch == 1:
            print(f"Epoch {epoch:3d} | Train Loss: {loss_train.item():.4f} | Val Loss: {loss_val.item():.4f}")

    print("\n结论：你可以清晰看到，随着训练推进，Train Loss 越来越小，但 Val Loss 却不降反升。")
    print("在工业界，我们通常会引入 Early Stopping 机制，当 Val Loss 连续多个 epoch 反弹时强行终止训练。")

if __name__ == "__main__":
    run_experiment()
