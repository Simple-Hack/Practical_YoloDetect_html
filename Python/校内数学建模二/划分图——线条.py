import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

# 读取CSV文件
df = pd.read_csv('111111.csv')

# 选取数据的一个子集（例如，每10个点取一个）
df_subset = df.iloc[::10, :]

# 提取x, y, z值
x = df_subset['x'].values
y = df_subset['y'].values
z = df_subset['z'].values
z = -z

# 创建规则网格
grid_x, grid_y = np.mgrid[min(x):max(x):100j, min(y):max(y):100j]

# 使用griddata进行插值
grid_z = griddata((x, y), z, (grid_x, grid_y), method='linear')

# 使用matplotlib绘制等高线图
fig, ax = plt.subplots()
cs = ax.contourf(grid_x, grid_y, grid_z, levels=100, cmap='viridis')
c = ax.contour(grid_x, grid_y, grid_z, colors='k', levels=cs.levels[::2])
# plt.clabel(c, inline=True, fontsize=8)

# 设置坐标轴标签和标题
ax.set_xlabel('由西向东(海里)', fontproperties="SimHei")
ax.set_ylabel('由南向北(海里)', fontproperties="SimHei")
ax.set_title('区域海底深度图', fontproperties="SimHei")

# 添加颜色条
plt.colorbar(cs)

# 在地形图上绘制分割线
plt.hlines(4.5, 0, 4, colors='r', linestyles='solid')
plt.hlines(2.5, 0, 2.5, colors='r', linestyles='solid')
plt.hlines(2, 2.5, 4, colors='r', linestyles='solid')
plt.vlines(1, 0, 2.5, colors='r', linestyles='solid')
plt.vlines(2.5, 0, 4.5, colors='r', linestyles='solid')

# 设置坐标轴范围
plt.xlim(0, max(x))
plt.ylim(0, max(y))

# 在左上角矩形内添加文本
plt.text(2, 4.75, '区域①', fontsize=12, ha='center', va='center', fontproperties="SimHei", bbox=dict(facecolor='white', alpha=1))
plt.text(1.25, 3.5, '区域②', fontsize=12, ha='center', va='center', fontproperties="SimHei", bbox=dict(facecolor='white', alpha=1))
plt.text(3.25, 3.25, '区域③', fontsize=12, ha='center', va='center', fontproperties="SimHei", bbox=dict(facecolor='white', alpha=1))
plt.text(0.5, 1.25, '区域④', fontsize=12, ha='center', va='center', fontproperties="SimHei", bbox=dict(facecolor='white', alpha=1))
plt.text(1.75, 1.25, '区域⑤', fontsize=12, ha='center', va='center', fontproperties="SimHei", bbox=dict(facecolor='white', alpha=1))
plt.text(3.25, 1, '区域⑥', fontsize=12, ha='center', va='center', fontproperties="SimHei", bbox=dict(facecolor='white', alpha=1))

# 显示图形
plt.show()