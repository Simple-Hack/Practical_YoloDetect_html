import math
import matplotlib.pyplot as plt
import numpy as np

def calculate_and_plot_lines(alpha, former_D, sei_ta, d):
    def cal_W(d, index):
        D = former_D - d * math.tan(alpha)
        if index == 1:
            return D * math.sin(sei_ta/2) / math.cos(sei_ta/2 + alpha)
        else:
            return D * math.sin(sei_ta/2) / math.cos(sei_ta/2 - alpha)
    
    return cal_W(d, 1) + cal_W(d, 2)

# 定义参数
alpha = 1.5 * math.pi / 180
former_D = 110
sei_ta_values = [90 * math.pi / 180,100*math.pi/180,110 * math.pi / 180, 120*math.pi/180,
                130 * math.pi / 180, 140*math.pi/180,150 * math.pi / 180]
alpha_values=[10 * math.pi / 180,20 * math.pi / 180,30 * math.pi / 180,40 * math.pi / 180,50 * math.pi / 180,60 * math.pi / 180,70 * math.pi / 180]
d_list = np.arange(-1000, 1000+1, 200)

# 创建一个空列表来存储所有计算结果
results = []

# 对于每个 sei_ta 计算结果
for sei_ta in sei_ta_values:
    results.append([calculate_and_plot_lines(alpha, former_D, sei_ta, d) for d in d_list])

# 绘制曲线
colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow','peru']
for i, result in enumerate(results):
    plt.plot(d_list, result, color=colors[i], label=f'{sei_ta_values[i]*180/math.pi:.1f}°')

# 设置图例
plt.legend()

# 设置坐标轴标签
plt.title('覆盖宽度与开角的关系',fontproperties="SimHei")
plt.xlabel('距离中心点距离(m)',fontproperties="SimHei")
plt.ylabel('覆盖宽度',fontproperties="SimHei")
plt.rcParams['font.family']=['SimHei']#关键是这句
# 显示图形
plt.grid(True)
plt.show()