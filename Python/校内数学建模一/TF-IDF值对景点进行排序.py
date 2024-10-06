import pandas as pd
import gensim
from gensim.corpora import Dictionary
from gensim.models import TfidfModel
from gensim.matutils import corpus2csc
import jieba
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

# 读取CSV文件
file_path = r'D:\VsFile\Python\啊_comment.csv'
data = pd.read_csv(file_path)

# 构建TF-IDF模型
all_texts = data['cleaned_content'].tolist()
dictionary = Dictionary(all_texts)
corpus = [dictionary.doc2bow(text) for text in all_texts]
tfidf_model = TfidfModel(corpus)
tfidf_corpus = tfidf_model[corpus]

# 计算主题词的TF-IDF值
scenic_areas = data['景点'].unique()
all_topic_keywords_tfidf = {}

# 定义主题标签
topics = ['名胜古迹', '自然风光', '历史文化', '现代建筑', '娱乐休闲']

for scenic_area in scenic_areas:
    print(f"Processing {scenic_area}...")
    scenic_area_data = data[data['景区名称'] == scenic_area]
    scenic_area_texts = scenic_area_data['cleaned_content'].tolist()
    scenic_area_corpus = [dictionary.doc2bow(text) for text in scenic_area_texts]
    scenic_area_tfidf_corpus = tfidf_model[scenic_area_corpus]
    
    # 计算每个景点的主题词TF-IDF值
    topic_keywords_tfidf = {}
    for topic in topics:
        topic_tfidf_values = []
        for doc_tfidf in scenic_area_tfidf_corpus:
            topic_tfidf = max((doc_tfidf.get(dictionary.token2id.get(topic, -1), 0)) for doc_tfidf in doc_tfidf)
            topic_tfidf_values.append(topic_tfidf)
        topic_keywords_tfidf[topic] = np.mean(topic_tfidf_values)
    
    all_topic_keywords_tfidf[scenic_area] = topic_keywords_tfidf

# 保存结果
result_df = pd.DataFrame(columns=['景区名称'] + topics)

# 将结果填充到DataFrame
for scenic_area, keywords_tfidf in all_topic_keywords_tfidf.items():
    result_df = pd.concat([result_df, pd.DataFrame({
        '景区名称': [scenic_area],
        **keywords_tfidf
    })], ignore_index=True)

# 保存结果到CSV
result_df.to_csv('scenic_area_tfidf.csv', index=False)

# 排序
sorted_result = result_df.sort_values(by=['名胜古迹'], ascending=False)
sorted_result.to_csv('scenic_area_sorted_by_tfidf.csv', index=False)