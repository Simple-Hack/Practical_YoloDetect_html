import pandas as pd
from pykrige.uk import UniversalKriging
import numpy as np
import matplotlib.pyplot as plt

# 读取数据并检查
data = pd.read_csv('111111.csv', names=['x', 'y', 'z'])

# 检查并删除非数字的行
data = data[pd.to_numeric(data['x'], errors='coerce').notnull()]
data = data[pd.to_numeric(data['y'], errors='coerce').notnull()]
data = data[pd.to_numeric(data['z'], errors='coerce').notnull()]

# 将数据转换为浮点数
data['x'] = data['x'].astype(float)
data['y'] = data['y'].astype(float)
data['z'] = data['z'].astype(float)

# 转换海里到米
data['x'] *= 1852
data['y'] *= 1852

# 准备数据
x = data['x'].values
y = data['y'].values
z = data['z'].values

# 接下来是你的克里金插值和绘图代码...
# 创建克里金插值模型
uk = UniversalKriging(x, y, z, variogram_model='linear')

# 设置网格密度
grid_x, grid_y = np.meshgrid(np.linspace(min(x), max(x), 100),
                             np.linspace(min(y), max(y), 100))

# 执行插值
z, ss = uk.execute('grid', grid_x, grid_y)

# 绘制等高线图
plt.figure(figsize=(10, 8))
CS = plt.contour(grid_x, grid_y, z, 15, linewidths=0.5, colors='k')
plt.clabel(CS, inline=1, fontsize=10)
plt.imshow(z, extent=(np.min(grid_x), np.max(grid_x), np.min(grid_y), np.max(grid_y)), origin='lower', cmap='terrain')
plt.colorbar()
plt.xlabel('X (m)')
plt.ylabel('Y (m)')
plt.title('Depth Map with Contours')
plt.show()