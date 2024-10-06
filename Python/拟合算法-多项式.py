import numpy as np
import matplotlib.pyplot as plt

x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
y = np.array([2.5, 4.5, 4.8, 5.5, 6.0, 7.0, 7.8, 8.0, 9.0, 9.5])

# 计算多项式回归系数
coefs = np.polyfit(x, y, 3)

# 使用np.poly1d函数来生成一个多项式拟合对象
poly = np.poly1d(coefs)

# 生成新的横坐标，使得拟合曲线更加平滑
new_x = np.linspace(min(x), max(x), 1000)

# 绘制拟合曲线
plt.scatter(x, y)
plt.plot(new_x, poly(new_x), color='red')

plt.show()
