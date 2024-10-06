
import pandas as pd
import matplotlib.pyplot as plt

# 定义文件路径
file_path = r'D:\VsFile\Python\scenic_area_topics_with_clusters.csv'

# 读取CSV文件
data = pd.read_csv(file_path)

# 统计每个聚类的数量
cluster_counts = data['聚类标签'].value_counts().sort_index()

# 创建饼图
plt.figure(figsize=(8, 6))
plt.pie(cluster_counts, labels=['历史建筑集群', '户外休闲集群', '缙云山集群', '民俗文化集群', '温泉休闲集群'],
        autopct='%1.1f%%', startangle=140)
plt.title('不同类型的景区占比')
plt.rcParams['font.sans-serif'] = ['SimHei'] # 用来正常显示中文标签SimHei
plt.rcParams['axes.unicode_minus'] = False # 用来正常显示负号
plt.show()