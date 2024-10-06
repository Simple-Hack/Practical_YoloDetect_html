import numpy as np
import matplotlib.pyplot as plt

x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
y = np.array([2.5, 4.5, 4.8, 5.5, 6.0, 7.0, 7.8, 8.0, 9.0, 9.5])

# 计算回归系数
slope, intercept = np.polyfit(x, y, 1)

# 绘制拟合曲线
plt.scatter(x, y)
plt.plot(x, slope * x + intercept, color='red')

plt.show()
