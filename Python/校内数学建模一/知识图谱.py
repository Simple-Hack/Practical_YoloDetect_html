import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter

# 读取数据
df = pd.read_csv('scenic_area_topics_with_clusters.csv')

# 处理缺失值，将聚类标签中的NaN替换为一个特定值，比如6（假设6代表“未分类”）
df['聚类标签'] = df['聚类标签'].fillna(6)

# 创建一个空的无向图
G = nx.Graph()

# 添加节点
for index, row in df.iterrows():
    G.add_node(row['景区名称'], cluster=row['聚类标签'])

# 获取不同的聚类标签
clusters = df['聚类标签'].unique()

# 定义颜色映射字典
color_map = {2: 'blue', 3: 'purple', 4: 'green', 5: 'orange', 6: 'gray',0:'red',1:'yellow'}

# 加载 CSV 文件
result_df = pd.read_csv('scenic_area_topics_with_clusters.csv')

# 定义优化后的关键词
optimized_keywords = {
    4: "大礼堂, 博物馆, 建筑, 三峡",
    2: "歌乐山, 景色, 森林公园, 爬山",
    3: "古镇, 磁器, 麻花, 小吃",
    0: "温泉, 环境, 服务, 水质",
    1: "博物馆, 三峡, 文物, 展览"
}

def draw_cluster(G, cluster, color, cluster_label):
    # 提取属于当前聚类的节点
    nodes_in_cluster = [n for n, d in G.nodes(data=True) if d['cluster'] == cluster]
    
    # 使用circular布局
    pos = nx.circular_layout(G.subgraph(nodes_in_cluster))
    
    # 设置画布背景颜色为乳白色
    ax = plt.gca()
    ax.set_facecolor('whitesmoke')  # 或者使用 'white' 为纯白色
    
    # 绘制节点
    nx.draw_networkx_nodes(G.subgraph(nodes_in_cluster), pos, node_size=2000, node_color=color, alpha=0.8)
    
    # 绘制标签
    nx.draw_networkx_labels(G.subgraph(nodes_in_cluster), pos, font_size=10, font_family="SimHei")
    
    # 在中心添加聚类的标签
    center_pos = {0: (0, 0)}  # 中心点坐标
    nx.draw_networkx_labels(G, center_pos, labels={0: cluster_label}, font_size=10, font_family="SimHei")
    
    # 设置标题
    plt.title(f"聚类 {cluster} 的景区")
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    plt.axis('off')
    
    # 显示图形
    plt.show()

# 对于每个聚类，创建一个新画布并绘制节点
for cluster in clusters:
    # 创建新的图形
    plt.figure(figsize=(10, 10))
    
    # 获取对应聚类的颜色
    color = color_map.get(cluster, 'gray')  # 如果聚类标签不在字典中，默认使用灰色
    
    # 获取优化后的关键词
    cluster_label = optimized_keywords.get(cluster, "未分类")
    
    # 调用绘制函数
    draw_cluster(G, cluster, color, cluster_label)

