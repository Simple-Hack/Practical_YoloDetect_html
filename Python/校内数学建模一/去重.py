# 导入pandas库，用于数据处理
import pandas as pd

# 读取评论数据
data = pd.read_csv('comments.csv')

# 去除数据中的重复项
data.drop_duplicates(inplace=True)

# 导入正则表达式和jieba分词库，用于文本清洗
import re
import jieba

def clean_text(text):
    """
    清洗文本数据，只保留中文字符
    参数:
        text: 待清洗的文本字符串
    返回值:
        清洗后的中文字符列表
    """
    # 只保留中文字符
    cleaned_text = re.sub(r'[^\u4e00-\u9fa5]', '', text)
    # 使用jieba对中文文本进行分词
    # 分词
    words = jieba.lcut(cleaned_text)
    return words

# 对评论数据中的用户评论列进行文本清洗
data['processed_text'] = data['用户评论'].apply(clean_text)

# 导入TF-IDF向量化器，用于文本向量化
from sklearn.feature_extraction.text import TfidfVectorizer

# 将同一景点的评论合并，并进行TF-IDF转换
# 合并同一景点的所有评论
grouped_data = data.groupby('景点')['processed_text'].apply(list).reset_index()
grouped_data['merged_text'] = grouped_data['processed_text'].apply(lambda x: ' '.join(x))

# 初始化TF-IDF向量化器
# TF-IDF向量化器
vectorizer = TfidfVectorizer(use_idf=True, tokenizer=lambda x: x, lowercase=False)
# 对合并后的评论文本进行TF-IDF转换
tfidf_matrix = vectorizer.fit_transform(grouped_data['merged_text'])

# 获取转换后的特征名称
# 获取特征名称
feature_names = vectorizer.get_feature_names_out()

def get_top_keywords(tfidf_vector, feature_names, top_n=10):
    """
    获取文本中排名前n的关键词
    参数:
        tfidf_vector: TF-IDF向量
        feature_names: 特征名称列表
        top_n: 需要返回的关键词数量
    返回值:
        排名前n的关键词列表
    """
    # 按照TF-IDF值降序排序，获取排名前n的关键词索引
    sorted_indices = tfidf_vector.argsort().flatten()[::-1]
    # 根据索引获取对应的关键词
    top_keywords = [feature_names[i] for i in sorted_indices[:top_n]]
    return top_keywords

# 对每个景点的评论，提取排名前10的关键词
grouped_data['keywords'] = [get_top_keywords(tfidf_matrix[i], feature_names) for i in range(len(grouped_data))]

# 将关键词和景点信息保存到文件
# 保存关键词到文件
grouped_data[['景点', 'keywords']].to_csv('keywords_by_location.csv', index=False)

# 导入KMeans聚类算法
from sklearn.cluster import KMeans

# 将TF-IDF矩阵转换为数组，以适应KMeans算法的要求
# 将TF-IDF矩阵转换为数组，用于K-means
tfidf_array = tfidf_matrix.toarray()

# 初始化KMeans聚类模型，设置聚类数目为3
# 进行K-means聚类
kmeans = KMeans(n_clusters=3)
# 对数据进行聚类
clusters = kmeans.fit_predict(tfidf_array)

# 将聚类结果添加到grouped_data中
# 将聚类结果添加到DataFrame中
grouped_data['cluster'] = clusters

# 将包含聚类结果的数据保存到文件
# 保存包含聚类信息的DataFrame
grouped_data.to_csv('clustered_data.csv', index=False)

# 打印每个景点的关键词和所属聚类
print(grouped_data[['景点', 'keywords', 'cluster']])