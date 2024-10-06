import matplotlib.pyplot as plt
from collections import defaultdict

# 创建字典并填充数据
dic = defaultdict(int)
dic['1'] = 4
dic['2'] = 23
dic['3'] = 20
dic['4'] = 62
dic['5'] = 42
dic['6'] = 9

# 提取分区名称和对应的值
names = list(dic.keys())
values = list(dic.values())

# 创建柱状图
plt.bar(names, values)

# 添加标题和坐标轴标签
plt.title('测线数量分布',fontproperties="SimHei")
plt.xlabel('分区',fontproperties="SimHei")
plt.ylabel('数量',fontproperties="SimHei")

# 显示图形
plt.show()