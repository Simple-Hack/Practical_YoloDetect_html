from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# 用于存储每个景点的平均主题分布
scenic_area_topic_distributions = {}

# 为每个景点提取平均主题分布
for scenic_area in scenic_areas:
    scenic_area_data = data[data['景区名称'] == scenic_area]
    lda = all_lda_models[scenic_area]
    corpus = [dictionary.doc2bow(text) for text in scenic_area_data['cleaned_content']]
    topic_distributions = [lda.get_document_topics(doc) for doc in corpus]
    avg_topic_distribution = np.mean([np.array([dist for _, dist in doc_topics]) for doc_topics in topic_distributions], axis=0)
    scenic_area_topic_distributions[scenic_area] = avg_topic_distribution

# 转换为可用于聚类的矩阵
X = np.array(list(scenic_area_topic_distributions.values()))

# 应用K-Means聚类
n_clusters = 5  # 可以调整簇的数量
kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(X)
labels = kmeans.labels_

# 计算轮廓系数评估聚类质量
silhouette_avg = silhouette_score(X, labels)
print("The average silhouette_score is :", silhouette_avg)

# 将聚类标签添加到结果DataFrame中
result_df['聚类标签'] = list(labels)

# 保存结果
result_df.to_csv('scenic_area_topics_with_clusters.csv', index=False)