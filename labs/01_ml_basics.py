# labs/01_ml_basics.py
# 对应第四章：机器学习基础闭环（线性回归最小示例）
# 目标：展示从数据划分 -> 模型训练 -> 评估指标的严谨环节。

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

def run_experiment():
    print("--- 机器学习基础：线性回归最小闭环 ---\n")
    
    # 1. 制造“假数据” (模拟房价)
    # X：房屋面积 (平方米)，y：价格 (万)
    np.random.seed(42)  # 保证结果可复现
    X = 2 * np.random.rand(100, 1) * 100 + 50  # 面积分布在 50~250 平米
    # 真实关系：价格 = 5 * 面积 + 20 + 噪音
    y = 5 * X + 20 + np.random.randn(100, 1) * 50 

    # 2. 数据划分：为什么必须分离“训练集”和“测试集”？
    # -> 避免模型“死记硬背”，验证其泛化能力。
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"数据总数: {len(X)} | 训练集: {len(X_train)} | 测试集: {len(X_test)}\n")

    # 3. 确立目标函数并训练模型 (即“算”的过程)
    model = LinearRegression()
    model.fit(X_train, y_train)

    # 模型学到的规律
    print(">> 模型学到的“规律”:")
    print(f"\t每增加1平米，价格增加: {model.coef_[0][0]:.2f} 万 (斜率/权重)")
    print(f"\t基础底价: {model.intercept_[0]:.2f} 万 (截距/偏差)\n")

    # 4. 可观测的误差指标评估 (避免用类比代替严谨)
    # 测试集上的预测结果
    y_pred = model.predict(X_test)
    
    # RMSE (均方根误差)：预测值与真实值平均相差多少万
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    # R2 Score：模型解释了多少数据的变异 (越接近 1 越好)
    r2 = r2_score(y_test, y_pred)

    print(">> 模型表现评估 (测试集):")
    print(f"\t均方根误差 (RMSE): {rmse:.2f} 万")
    print(f"\tR² 分数: {r2:.4f}\n")
    
    print("结论：一旦指标达到业务可接受的阈值，训练完成。")

if __name__ == "__main__":
    run_experiment()
