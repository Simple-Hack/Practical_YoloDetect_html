""" bp神经网络测试 实现简单函数拟合任务 """
import numpy as np
from matplotlib import cycler, pyplot as plt
from net import BPNet
#from Plot.styles import mp_seaborn_light
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

mp_seaborn_base = {
    'figure.figsize': (8, 8),
    'figure.dpi': 100,
    'axes.grid': True,
    'axes.labelpad': 14,
    'axes.titlepad': 16,
    'axes.facecolor': "#EDEDF2",
    'axes.titlecolor': '#333333',
    'axes.labelcolor': '#535353',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.spines.bottom': False,
    'axes.spines.left': False,
    'ytick.color': '#535353',
    'ytick.left': False,
    'ytick.direction': "in",
    'xtick.color': '#535353',
    'xtick.bottom': False,
    'xtick.direction': "in",
    'grid.color': "white",
    'grid.linewidth': 1,
    'grid.alpha': 0.4,
    'text.color': "535353",
    'legend.edgecolor': 'w',
    'scatter.edgecolors': 'w',
    'patch.force_edgecolor': True,
    'patch.edgecolor': 'white',
    'patch.linewidth': 0.6,
    'boxplot.capprops.color': '#535353',
    'boxplot.boxprops.color': 'white',
    'boxplot.boxprops.linewidth': 0.6,
    'boxplot.whiskerprops.color': '#535353',
    'boxplot.whiskerprops.linewidth': 0.6,
    'boxplot.whiskerprops.linestyle': ':',
    'boxplot.medianprops.color': 'white',
    'boxplot.meanprops.color': 'white',
    'boxplot.meanprops.markeredgecolor': 'white',
    'boxplot.meanprops.markerfacecolor': 'white',
}  # seaborn 风格
def mp_seaborn_light():
    """ seaborn 清新配色 """
    style = mp_seaborn_base.copy()
    style['axes.prop_cycle'] = cycler('color', ['fb9489', 'a9ddd4', '9ec3db', 'cbc7de', 'fdfcc9'])
    return style

# 生成数据
x = np.arange(0, np.pi, 0.1).reshape(-1, 1)
y = np.sin(x)

# 创建bp神经网络并训练
bp = BPNet(1, [3], 1, "tanh")
bp.train(x, y, 1000, lr=0.01)

new_x = np.arange(0, np.pi, 0.1).reshape(-1, 1)
new_y = np.sin(new_x)
print('\n预测结果:\n', bp.predict(new_x))
print('\n准确率:\n', bp.evaluate(new_x, new_y))

# 绘制图像
plt.style.use(mp_seaborn_light())
bp.plot_network()
bp.plot_data(new_x, new_y)
plt.show()