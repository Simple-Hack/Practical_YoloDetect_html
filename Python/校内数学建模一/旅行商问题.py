import numpy as np
from math import radians, cos, sin, asin, sqrt
from sko.GA import GA_TSP
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MaxNLocator
# 加载经纬度数据
excel_file = r"D:\qq\2385786690\FileRecv\更新后的景区数据.xlsx"
df = pd.read_excel(excel_file)

# 获取推荐的景区名列表
recommended_names = [
    "重庆綦江古剑山风景区",
    "重庆丰都南天湖景区",
    "重庆涪陵武陵山国家森林公园",
    "重庆歌乐山森林公园",
    "重庆巫溪红池坝景区",
    '重庆石柱千野草场',
    '重庆丰都名山风景区',
    '重庆石柱大风堡景区',
]

# 创建空矩阵用于存储经纬度信息
recommended_longitude = []
recommended_latitude = []

# 查找推荐的景区名及其对应的经纬度
for name in recommended_names:
    row = df[df["名称"] == name]
    if not row.empty:
        recommended_longitude.append(row["经度"].values[0])
        recommended_latitude.append(row["纬度"].values[0])

# 将经纬度信息转换为numpy数组
longitude = np.array(recommended_longitude)
latitude = np.array(recommended_latitude)

num_points = len(longitude)

# 定义 Haversine 公式来计算两点间的距离
def haversine(coord1, coord2):
    R = 6371  # 地球平均半径，单位为公里
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    return c * R

# 构建距离矩阵
distance_matrix = np.zeros((num_points, num_points))
for i in range(num_points):
    for j in range(i, num_points):
        if i == j:
            distance_matrix[i][j] = 0
        else:
            distance_matrix[i][j] = haversine((latitude[i], longitude[i]), (latitude[j], longitude[j]))
        distance_matrix[j][i] = distance_matrix[i][j]

# 直接计算总距离，不考虑好感度
def cal_total_distance(routine, distance_matrix):
    num_points, = routine.shape
    total_distance = 0
    # 计算总距离
    for i in range(num_points):
        current = routine[i % num_points]
        next_point = routine[(i + 1) % num_points]
        distance = distance_matrix[current, next_point]
        total_distance += distance
    return total_distance

# 初始化遗传算法，使用新的目标函数
ga_tsp = GA_TSP(func=lambda x: cal_total_distance(x, distance_matrix),
                n_dim=num_points, size_pop=50, max_iter=30, prob_mut=0.01)

# 初始化遗传算法，使用新的目标函数

# 执行遗传算法
best_points, best_distance = ga_tsp.run()

# 创建一个字典来映射索引到景区名称
index_to_name = {i: name for i, name in enumerate(recommended_names)}
##########################
mp_white_base = {
    'figure.figsize': (8, 8),
    'figure.dpi': 100,
    'axes.grid': True,
    'axes.labelpad': 14,
    'axes.titlepad': 16,
    'axes.titlecolor': '#333333',
    'axes.labelcolor': '#535353',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'ytick.color': '#535353',
    'ytick.direction': "in",
    'xtick.color': '#535353',
    'xtick.direction': "in",
    'grid.linewidth': 1,
    "grid.alpha": 0.25,
    'lines.linewidth': 1,
    'lines.markersize': 2,
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
}  # 白底风格
""" 绘图风格包 """
from matplotlib import cycler
def mp_white_light():
    """ 白底 清新配色 """
    style = mp_white_base.copy()
    style['axes.prop_cycle'] = cycler('color', ['fb9489', 'a9ddd4', '9ec3db', 'cbc7de', 'fdfcc9'])
    return style


#########################
# 修改输出结果的部分，将索引转换为景区名称
best_route_names = [index_to_name[index] for index in best_points]
print(f"Best route by names: {best_route_names}")
print(f"Best distance: {best_distance}")

# 计算经纬度的边界并增加缓冲
longitude_min, longitude_max = np.min(longitude), np.max(longitude)
latitude_min, latitude_max = np.min(latitude), np.max(latitude)
buffer = 0.8  # 缓冲量，根据实际情况调整


# 绘制迭代过程中的适应度变化图
plt.figure(figsize=(10, 6))
plt.plot(ga_tsp.fitness_history)
plt.title('适应度随迭代次数的变化')
plt.xlabel('迭代次数')
plt.ylabel('适应度')
plt.grid(True)
plt.show()

plt.figure(figsize=(20, 14))
ax = plt.gca()  # 获取当前的Axes实例
ax.xaxis.set_major_locator(MaxNLocator(nbins=20, steps=[1, 2, 5, 10]))  # 设置刻度定位器
best_points_ = np.concatenate([best_points, [best_points[0]]])
best_points_coordinate = np.vstack((longitude[best_points_], latitude[best_points_])).T
plt.plot(best_points_coordinate[:, 0], best_points_coordinate[:, 1], 'o-r')
plt.xlim(longitude_min - 0.3, longitude_max + 0.3)
plt.ylim(latitude_min - buffer, latitude_max + buffer)

# 添加每个点的景区名称  
for i, txt in enumerate(best_route_names):  
    # 使用 xytext 和 arrowprops 调整文本位置和样式  
    if txt == "重庆涪陵武陵山国家森林公园":  
        # 仅对 "涪陵武陵山国家森林公园" 进行偏移  
        offset = (0, -5)  # 增加垂直方向上的偏移量  
    elif txt=='重庆丰都南天湖景区':
        offset = (0, 8)
    else:
        offset = (0, 0)  # 其他标签不偏移  
  
    # 直接在annotate中使用offset  
    plt.annotate(txt,  
                 xy=(best_points_coordinate[i, 0], best_points_coordinate[i, 1]),  
                 xytext=(offset[0], offset[1]),  
                 textcoords='offset points',  # 指定xytext的坐标系统  
                 ha='center', va='top',  # 尝试使用居中对齐和顶部对齐  
                 bbox=dict(boxstyle="round,pad=0.0", fc="w"),  # 文本框样式  
                 arrowprops=None)  # 禁用箭头  
# 设置坐标轴范围

plt.title('最好路径')
plt.xlabel('经度')
plt.ylabel('维度')
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.show()