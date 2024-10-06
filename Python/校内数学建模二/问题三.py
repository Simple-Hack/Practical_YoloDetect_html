import math
import openpyxl
from sympy.solvers import solve
from sympy import Symbol
alpha = 1.5 * math.pi / 180
sei_ta = 2 * math.pi / 3
former_D=110
length=4*1852
width=2*1852
dis=[0 for _ in range(114)]
workbook = openpyxl.Workbook()
worksheet = workbook.active
x = Symbol("x")
dis[0]=float(solve(length/2+x/math.cos(alpha)-(former_D-x*math.tan(alpha))*math.sin(sei_ta)/math.cos(sei_ta/2+alpha),x)[0])

def cal_W(d,index):
    D=former_D-d*math.tan(alpha)
    W=None
    if index==1:
        W=D*math.sin(sei_ta/2)/math.cos(sei_ta/2+alpha)
    else:
        W=D*math.sin(sei_ta/2)/math.cos(sei_ta/2-alpha)
    return W
    
ind=0
for i in range(1,114):
    d=Symbol('d')
    dis[i]=float(solve(cal_W(d,1)-(d-dis[i-1])/math.cos(alpha)+cal_W(dis[i-1],2)-(1/10) *(cal_W(d,1)+cal_W(d,2)),d)[0])
    if dis[i]>=length/2:
        break
    ind+=1
for i in range(ind+1):
    print(dis[i]/math.cos(alpha),end=' ')
    worksheet.cell(row=i+1,column=1).value = f'{dis[i]/math.cos(alpha):.2f}'
workbook.save("问题三.xlsx")
print(f'\n总的线条数为:{ind+1},长度总和为:{(ind+1)*width}')

import matplotlib.pyplot as plt

data = [dis[i]/math.cos(alpha) for i in range(ind+1)]
# 绘制垂直线
plt.vlines(data,ymin=0,ymax=width, colors='blue')

# 添加标题和标签
plt.title('测线',fontproperties="SimHei")
plt.xlabel('与中心点距离(m) ',fontproperties="SimHei")
plt.ylabel('测线长度(m)',fontproperties="SimHei")
# 显示图表
plt.show()


