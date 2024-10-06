import pandas as pd
import gensim
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import numpy as np
np.random.seed(2018)
import nltk
import re
from nltk.corpus import stopwords
from gensim import corpora, models
import jieba
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import emoji

# 读取CSV文件
file_path = r'D:\VsFile\Python\啊_comment.csv'
data = pd.read_csv(file_path)

# 加载中文停用词
def load_stopwords(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        stopwords = set(word.strip() for word in file.readlines())
    return stopwords

# 清洗评论内容
def clean_text(text):
    # 仅保留中文字符、空格，并去除表情符号
    pattern = re.compile("[^\u4e00-\u9fa5]")  # 匹配非中文字符
    text = emoji.demojize(text)
    text = re.sub(pattern, "", text)
    # 分词
    tokens = jieba.lcut(text)
    # 去除停用词
    stop_words = load_stopwords(r'D:\VsFile\Python\baidu_stopwords.txt')
    # 添加单字作为停用词
    single_chars = set([t for t in tokens if len(t) == 1])
    stop_words.update(single_chars)
    cleaned_tokens = [token for token in tokens if token not in stop_words and token.isalpha()]
    # 如果清洗后为空，则保留一个特殊标记
    if not cleaned_tokens:
        cleaned_tokens = ['<empty>']
    return cleaned_tokens

# 删除重复的行，保留首次出现的行
data = data.drop_duplicates()
# 应用清洗函数
data['cleaned_content'] = data['用户评论'].apply(clean_text)
print('清洗数据结束')

# 针对每个景点提取主题
scenic_areas = data['景点'].unique()
all_topic_keywords = {}
all_lda_models = {}

# 对每个景点提取主题
for scenic_area in scenic_areas:
    print(f"Processing {scenic_area}...")
    scenic_area_data = data[data['景点'] == scenic_area]
    
    # 创建词典
    dictionary = corpora.Dictionary(scenic_area_data['cleaned_content'])
    
    # 创建语料库
    corpus = [dictionary.doc2bow(text) for text in scenic_area_data['cleaned_content']]
    
    # 设置LDA模型参数 - 调整主题数量为2
    chunksize = 2000
    passes = 20
    iterations = 400
    eval_every = None
    
    # 训练LDA模型
    lda = gensim.models.ldamodel.LdaModel(
        corpus=corpus,
        id2word=dictionary,
        num_topics=2,  # 调整为2个主题
        random_state=100,
        update_every=1,
        chunksize=chunksize,
        passes=passes,
        alpha='auto',
        per_word_topics=True,
        iterations=iterations,
        eval_every=eval_every
    )
    all_lda_models[scenic_area] = lda
    
    # 获取主题关键词
    topic_keywords = []
    for i in range(2):  # 只获取2个主题
        keywords = [kw[0] for kw in lda.show_topic(i, topn=10)]
        topic_keywords.append(keywords)
    
    # 返回主题关键词
    all_topic_keywords[scenic_area] = topic_keywords

# 初始化一个新的 DataFrame 用于存储每个景区的信息
scenic_area_topics_df = pd.DataFrame(columns=['景区名称', '主题1关键词', '主题2关键词'])

# 将结果合并到新的 DataFrame
for scenic_area, keywords in all_topic_keywords.items():
        scenic_area_topics_df = pd.concat([scenic_area_topics_df, pd.DataFrame({
            '景区名称': [scenic_area],
            '主题1关键词': [keywords[0]],
            '主题2关键词': [keywords[1]]
        })], ignore_index=True)

# 保存结果
scenic_area_topics_df.to_csv('scenic_area_topics.csv', index=False)
print('主题关键词提取完成')

# 用于存储每个景点的平均主题分布
scenic_area_topic_distributions = {}

# 为每个景点提取平均主题分布
for scenic_area in scenic_areas:
    scenic_area_data = data[data['景点'] == scenic_area]
    dictionary = corpora.Dictionary(scenic_area_data['cleaned_content'])
    lda = all_lda_models[scenic_area]
    corpus = [dictionary.doc2bow(text) for text in scenic_area_data['cleaned_content']]
    topic_distributions = [lda.get_document_topics(doc) for doc in corpus]
    # 创建一个空的二维数组，形状为 (文档数量, 主题数量)
    num_topics = lda.num_topics
    num_docs = len(topic_distributions)
    topic_distributions_array = np.zeros((num_docs, num_topics))

    # 填充数组
    for i, doc_topics in enumerate(topic_distributions):
        for topic_id, prob in doc_topics:
            topic_distributions_array[i, topic_id] = prob

    # 计算平均主题分布
    avg_topic_distribution = np.mean(topic_distributions_array, axis=0)
    scenic_area_topic_distributions[scenic_area] = avg_topic_distribution
    # 在转换为可用于聚类的矩阵前打印scenic_area_topic_distributions的长度
    print(len(scenic_area_topic_distributions))

# 转换为可用于聚类的矩阵
X = np.array(list(scenic_area_topic_distributions.values()))
# 打印X矩阵的形状
print(X.shape)
# 应用K-Means聚类
n_clusters = 5  # 可以调整簇的数量
kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(X)
labels = kmeans.labels_
# 在应用K-Means聚类后打印labels的长度
print(len(labels))
# 计算轮廓系数评估聚类质量
# 打印scenic_area_topics_df的行数
print(len(scenic_area_topics_df))
silhouette_avg = silhouette_score(X, labels)
print("The average silhouette_score is :", silhouette_avg)

# 将聚类标签添加到结果DataFrame中
# 确保聚类标签的数量与景点数量一致
scenic_area_topics_df['聚类标签'] = list(labels)

# 保存结果
scenic_area_topics_df.to_csv('scenic_area_topics_with_clusters.csv', index=False)
print('主题关键词聚类完成')