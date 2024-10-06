import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.manifold import TSNE
import numpy as np
# 加载 CSV 文件
result_df = pd.read_csv('scenic_area_topics_with_clusters.csv')

# 将主题关键词列从字符串转换为列表
result_df['主题1关键词'] = result_df['主题1关键词'].apply(lambda x: eval(x))
result_df['主题2关键词'] = result_df['主题2关键词'].apply(lambda x: eval(x))

# 创建一个字典来存储每个聚类的标签
cluster_labels = {}

# 对每个聚类进行迭代
for cluster_id in result_df['聚类标签'].unique():
    # 选择属于当前聚类的所有行
    cluster_data = result_df[result_df['聚类标签'] == cluster_id]
    
    # 初始化一个字典来统计每个主题的出现次数
    topic_counts = Counter()
    
    # 遍历每个景点的主题
    for topics in cluster_data[['主题1关键词', '主题2关键词']].values:
        # 将主题列表转换为元组，便于计数
        topic_counts.update([tuple(topic) for topic in topics])
    
    # 找出最常见的主题
    most_common_topic = topic_counts.most_common(1)[0][0]
    
    # 为聚类分配一个描述性的标签
    # 这里使用最常见的主题关键词作为标签的一部分
    cluster_label = f"Cluster_{cluster_id}_with_Topics_{', '.join(most_common_topic)}"
    
    # 存储标签
    cluster_labels[cluster_id] = cluster_label

# 输出每个聚类的标签
for cluster_id, label in cluster_labels.items():
    print(f"Cluster {cluster_id}: {label}")

# 使用t-SNE降维
topics = result_df[['主题1关键词', '主题2关键词']].values.tolist()
labels = result_df['聚类标签'].values
scenic_names = result_df['景区名称'].values

# 将主题关键词转换为一个统一的列表
all_topics = [item for sublist in topics for topic_list in sublist for item in topic_list]

# 创建一个词典来映射主题关键词到数字标识
topic_to_id = {topic: idx for idx, topic in enumerate(set(all_topics))}
id_to_topic = {idx: topic for topic, idx in topic_to_id.items()}

# 将主题关键词转换为数字标识
topics_numeric = []
for topic_list1, topic_list2 in topics:
    # 将两个主题列表合并为一个列表
    combined_topics = topic_list1 + topic_list2
    # 转换为数字标识
    numeric_topics = [topic_to_id[topic] for topic in combined_topics]
    topics_numeric.append(numeric_topics)

# 计算每个景点的主题分布
topic_distributions = []
for sublist in topics_numeric:
    distribution = [0] * len(topic_to_id)
    for topic_id in sublist:
        distribution[topic_id] += 1
    topic_distributions.append(distribution)

# 将主题分布转换为NumPy数组
topic_distributions_np = np.array(topic_distributions)
tsne = TSNE(n_components=2, verbose=1, perplexity=40, n_iter=300)
tsne_results = tsne.fit_transform(topic_distributions_np)

# 手动创建描述性标签映射
custom_cluster_labels = {
    4: "历史建筑集群",
    3: "户外休闲集群",
    1: "缙云山集群",
    0: "民俗文化集群",
    2: "温泉休闲集群"
}

# 使用 custom_cluster_labels 映射更新 labels 数组
labels_desc = [custom_cluster_labels.get(label, f"未知集群_{label}") for label in labels]
# 创建散点图
plt.figure(figsize=(35, 28))  # 增加尺寸
sns.scatterplot(
    x=tsne_results[:,0], y=tsne_results[:,1],
    hue=labels_desc,
    palette=sns.color_palette("hls", len(set(labels_desc))),  # 根据聚类数量调整颜色数量
    legend="full",
    alpha=0.5,  # 增加点的不透明度，以便在较大的图表中更清楚地看到
    s=100  # 调整点的大小，以便在较大的图表中更清楚地看到
)


# 在图上标注每个景点的名称，并使用箭头指向
for i in range(len(scenic_names)):
    # 使用annotate()函数添加带箭头的文本标注
    plt.annotate(scenic_names[i],
                 (tsne_results[i,0], tsne_results[i,1]),
                 textcoords="offset points",  # 使用偏移点作为坐标系统
                 xytext=(0,10),  # 文本相对于点的偏移量
                 ha='center',  # 水平对齐方式
                 fontsize=4,
                 arrowprops=dict(arrowstyle="->"))  # 箭头属性

# 显示图表
plt.figure(dpi=3000)  # 设置dpi为300，可以根据需要调整
plt.rcParams['font.sans-serif'] = ['SimHei'] # 用来正常显示中文标签SimHei
plt.rcParams['axes.unicode_minus'] = False # 用来正常显示负号
plt.title(f'具有t-SNE的聚类散点图(景区总数: {len(scenic_names)})')
plt.show()
# Cluster 4: 历史建筑集群
# Cluster 3: 户外休闲集群
# Cluster 1: 缙云山集群
# Cluster 0: 民俗文化集群
# Cluster 2: 温泉休闲集群

