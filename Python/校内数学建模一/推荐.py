import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 读取CSV文件
df = pd.read_csv(r'D:\VsFile\Python\scenic_area_topics_with_clusters.csv')

# 处理关键词列，将字符串转换为列表
df['主题1关键词'] = df['主题1关键词'].str.strip('[]').str.split(',')
df['主题2关键词'] = df['主题2关键词'].str.strip('[]').str.split(',')

# 合并主题1和主题2关键词
df['关键词'] = df['主题1关键词'] + df['主题2关键词']

# 将关键词列表转换为字符串，以便TF-IDF向量化
df['关键词'] = df['关键词'].apply(lambda x: ' '.join(x))

# 初始化TF-IDF向量化器
vectorizer = TfidfVectorizer()

# 构建TF-IDF矩阵
tfidf_matrix = vectorizer.fit_transform(df['关键词'])

# 定义一个函数来推荐景点
def recommend_scenic_areas(user_keywords):
    # 将用户输入的关键词转换为TF-IDF向量
    user_tfidf = vectorizer.transform([' '.join(user_keywords)])
    
    # 计算用户关键词与所有景点关键词的余弦相似度
    similarity_scores = cosine_similarity(user_tfidf, tfidf_matrix).flatten()
    
    # 获取相似度得分最高的前N个景点的索引
    top_n_indices = similarity_scores.argsort()[::-1][:5]  # 返回前5个景点
    
    # 返回得分最高的景点名称
    return df.loc[top_n_indices, '景区名称'].tolist()

# 测试推荐函数
user_keywords = ['历史','避暑']
recommended_areas = recommend_scenic_areas(user_keywords)
print("推荐的景点:", recommended_areas)