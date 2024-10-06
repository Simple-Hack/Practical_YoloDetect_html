import math
import matplotlib.pyplot as plt
import numpy as np

sei_ta_values = [90 * math.pi / 180,100*math.pi/180,110 * math.pi / 180, 120*math.pi/180,
                130 * math.pi / 180, 140*math.pi/180,150 * math.pi / 180]
alpha_values=[10 * math.pi / 180,20 * math.pi / 180,30 * math.pi / 180,40 * math.pi / 180,50 * math.pi / 180,60 * math.pi / 180,70 * math.pi / 180]


def cal_depth(x):
    former_D=70
    return former_D-x*math.sin(1.5*math.pi/180)

def cal_width(x,alpha,sei_ta):
    return cal_depth(x)*math.sin(sei_ta/2)*(1/math.cos(sei_ta/2 + alpha) + 1/math.cos(sei_ta/2 - alpha))

def cal_eta(x,i,D,alpha,sei_ta):
    former_W2=cal_depth(D[i-1])*math.sin(sei_ta/2)/math.cos(sei_ta/2 - alpha)
    cur_W1=cal_depth(x)*math.sin(sei_ta/2)/math.cos(sei_ta/2 + alpha)
    up=cur_W1+former_W2-200/math.cos(alpha)
    down=cal_width(D[i-1],alpha,sei_ta)
    return up/down *100

# 定义参数
former_D = 110
sei_ta_values = [90 * math.pi / 180,100*math.pi/180,110 * math.pi / 180, 120*math.pi/180,
                130 * math.pi / 180, 140*math.pi/180,150 * math.pi / 180]
alpha_values=[0.5 * math.pi / 180,1 * math.pi / 180,1.5 * math.pi / 180,2 * math.pi / 180,2.5 * math.pi / 180,3*math.pi/180]
d_list = np.arange(-1000, 1000+1, 200)

# 创建一个空列表来存储所有计算结果
eta_results = []

# 对于每个 alpha 计算结果
count=1
for alp in alpha_values:
    eta_results.append([cal_eta(d_list[1], count, d_list, alp,sei_ta_values[3]) for d in d_list[1:]])
    count+=1

# 绘制曲线
#colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow','peru']
colors = ['blue', 'green', 'red', 'cyan', 'magenta','peru']
for i, result in enumerate(eta_results):
    plt.plot(d_list[1:], result, color=colors[i], label=f'{alpha_values[i]*180/math.pi:.1f}°')

# 设置图例
plt.legend(loc='upper right')
# 设置坐标轴标签
plt.title('重叠率与坡度的关系',fontproperties="SimHei")
plt.xlabel('距离中心点距离(m)',fontproperties="SimHei")
plt.ylabel('重叠率(%)',fontproperties="SimHei")
plt.xlim(-1000,1200)
plt.rcParams['font.family']=['SimHei']#关键是这句
# 显示图形
plt.grid(True)
plt.show()

