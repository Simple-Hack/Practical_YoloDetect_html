import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import math
from sympy import solve, Symbol
import matplotlib.pyplot as plt

# 定义颜色列表
colors = ['r', 'g', 'b', 'c', 'm', 'y']

# 海里到米的转换系数
nautical_mile_to_meter = 1852

# 读取 CSV 文件
data = pd.read_csv('111111.csv', names=['x', 'y', 'z'], skiprows=1)

# 将 x, y 列转换为米
data['x'] = data['x'] * nautical_mile_to_meter
data['y'] = data['y'] * nautical_mile_to_meter

def calculate_and_plot_lines(alpha, length, width, former_D):
    re = []
    sei_ta = 2 * math.pi / 3
    dis = [0 for _ in range(300)]
    x = Symbol('x')
    # 计算第一个点的距离
    dis[0] = float(solve(length/2 + x/math.cos(alpha) - (former_D - x*math.tan(alpha)) * math.sin(sei_ta) / math.cos(sei_ta/2 + alpha), x)[0])
    re.append(dis[0])
    
    def cal_W(d, index):
        D = former_D - d * math.tan(alpha)
        if index == 1:
            return D * math.sin(sei_ta/2) / math.cos(sei_ta/2 + alpha)
        else:
            return D * math.sin(sei_ta/2) / math.cos(sei_ta/2 - alpha)

    ind = 0
    for i in range(1, 300):
        d = Symbol('d')
        dis[i] = float(solve(cal_W(d, 1) - (d - dis[i-1]) / math.cos(alpha) + cal_W(dis[i-1], 2) - (1/10) * (cal_W(d, 1) + cal_W(d, 2)), d)[0])
        if dis[i] >= length/2:
            break
        re.append(dis[i])
        ind += 1

    for i in range(ind+1):
        print(dis[i] / math.cos(alpha), end=' ')

    return ind+1, (ind+1)*width, re

def fit_region(data, x_min, x_max, y_min, y_max, x_or_y, id):
    # 筛选出符合条件的数据
    filtered_data = data[
        (data['x'] >= x_min) & (data['x'] <= x_max) &
        (data['y'] >= y_min) & (data['y'] <= y_max)
    ]
    
    if x_or_y == 'x':
        # 如果 x 是自变量
        x_filtered = filtered_data['x'].values.reshape(-1, 1)
        y_filtered = filtered_data['z'].values
    elif x_or_y == 'y':
        # 如果 y 是自变量
        x_filtered = filtered_data['y'].values.reshape(-1, 1)
        y_filtered = filtered_data['z'].values
    else:
        raise ValueError("x_or_y must be either 'x' or 'y'")
    y_filtered = -filtered_data['z'].values
    
    # 使用线性回归模型进行拟合
    model = LinearRegression()
    model.fit(x_filtered, y_filtered)
    
    # 计算斜率
    slope = model.coef_[0]
    
    # 计算中心点
    center_x = np.mean(x_filtered)
    center_y = model.predict([[center_x]])[0]
    
    # 计算 R^2
    r_squared = model.score(x_filtered, y_filtered)
    
    return math.atan(abs(slope)), -center_y, model, r_squared, (abs(x_max-x_min), abs(y_max-y_min))

regions = [
    {'x_min': 0 * nautical_mile_to_meter, 'x_max': 4 * nautical_mile_to_meter, 'y_min': 4.5 * nautical_mile_to_meter, 'y_max': 5 * nautical_mile_to_meter, 'x_or_y': 'y', 'id': 1},
    {'x_min': 0 * nautical_mile_to_meter, 'x_max': 2.5 * nautical_mile_to_meter, 'y_min': 2.5 * nautical_mile_to_meter, 'y_max': 4.5 * nautical_mile_to_meter, 'x_or_y': 'y', 'id': 2},
    {'x_min': 2.5 * nautical_mile_to_meter, 'x_max': 4 * nautical_mile_to_meter, 'y_min': 2 * nautical_mile_to_meter, 'y_max': 4.5 * nautical_mile_to_meter, 'x_or_y': 'x', 'id': 3},
    {'x_min': 0 * nautical_mile_to_meter, 'x_max': 1 * nautical_mile_to_meter, 'y_min': 0 * nautical_mile_to_meter, 'y_max': 2.5 * nautical_mile_to_meter, 'x_or_y': 'y', 'id': 4},
    {'x_min': 1 * nautical_mile_to_meter, 'x_max': 2.5 * nautical_mile_to_meter, 'y_min': 0 * nautical_mile_to_meter, 'y_max': 2.5 * nautical_mile_to_meter, 'x_or_y': 'x', 'id': 5},
    {'x_min': 2.5 * nautical_mile_to_meter, 'x_max': 4 * nautical_mile_to_meter, 'y_min': 0 * nautical_mile_to_meter, 'y_max': 2 * nautical_mile_to_meter, 'x_or_y': 'x', 'id': 6},
    # 添加更多区域...
]

sum_lines = 0
sum_length = 0
# 循环拟合每个区域
plt.figure()
plt.title('测线区域图', fontproperties="SimHei")
plt.xlabel('x(n mile)', fontproperties="SimHei")
plt.ylabel('y(n mile)', fontproperties="SimHei")

for i, region in enumerate(regions):
    alpha, center, model, r_squared, ran = fit_region(data, **region)

    print(f"Region: x in [{region['x_min'] / nautical_mile_to_meter:.2f}, {region['x_max'] / nautical_mile_to_meter:.2f}] nautical miles, y in [{region['y_min'] / nautical_mile_to_meter:.2f}, {region['y_max'] / nautical_mile_to_meter:.2f}] nautical miles")
    print(f"alpha: {alpha}")
    print(f"Center: {center}")
    print(f"R^2: {r_squared}\n")
    
    color = colors[i % len(colors)]  # 获取颜色
    
    if region['x_or_y'] == 'x':
        line, length, res = calculate_and_plot_lines(alpha, ran[0], ran[1], center)
        sum_lines += line
        sum_length += length
        print(f'测线数为{line}')
        if region['id'] == 5:
            # res=res[:-5]
            res = res
        elif region['id'] == 6:
            # res=res[:-3]
            res = res
        for i, da in enumerate(res):
            res[i] = res[i] / nautical_mile_to_meter + (region['x_min'] / 1852 + region['x_max'] / 1852) / 2
            res[i] = (region['x_min'] + region['x_max']) / 1852 - res[i]

        plt.vlines(res, region['y_min'] / 1852, region['y_max'] / 1852, colors=color, linestyles='solid', label='')
    else:
        line, length, res = calculate_and_plot_lines(alpha, ran[1], ran[0], center)
        sum_length += length
        sum_lines += line
        print(f'测线数为{line}')
        for i, da in enumerate(res):
            res[i] = res[i] / nautical_mile_to_meter + (region['y_min'] / 1852 + region['y_max'] / 1852) / 2
            res[i] = (region['y_min'] + region['y_max']) / 1852 - res[i]
        plt.hlines(res, region['x_min'] / 1852, region['x_max'] / 1852, colors=color, linestyles='solid', label='')

plt.show()
print(f'总数为：{sum_lines},总长度为：{sum_length/1852}')