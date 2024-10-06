import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt

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

# 定义一个函数来推荐景点，现在接受关键词及其权重
def recommend_scenic_areas(user_keywords, weights):
    # 根据权重调整关键词的频率
    weighted_keywords = []
    for keyword, weight in zip(user_keywords, weights):
        weighted_keywords.extend([keyword] * int(weight * 10))  # 假设权重范围在0-1之间，乘以10是为了增加频率
    
    # 将加权后的关键词转换为TF-IDF向量
    user_tfidf = vectorizer.transform([' '.join(weighted_keywords)])
    
    # 计算用户关键词与所有景点关键词的余弦相似度
    similarity_scores = cosine_similarity(user_tfidf, tfidf_matrix).flatten()
    
    # 获取相似度得分最高的前N个景点的索引
    top_n_indices = similarity_scores.argsort()[::-1][:8]  # 返回前5个景点
    
    # 返回得分最高的景点名称及其相似度分数
    recommended_areas = []
    for idx in top_n_indices:
        recommended_areas.append({
            '景区名称': df.loc[idx, '景区名称'],
            '相似度得分': similarity_scores[idx],
            '聚类标签': df.loc[idx, '聚类标签'],
            '主题1关键词': df.loc[idx, '主题1关键词'],
            '主题2关键词': df.loc[idx, '主题2关键词']
        })
    
    return recommended_areas

# 测试推荐函数，现在传入关键词和它们的权重
user_keywords = ['爬山', '避暑','夏天']
weights = [0.4, 0.3,0.3]  # 露营比避暑更重要
recommended_areas = recommend_scenic_areas(user_keywords, weights)

# 打印推荐结果
print("推荐的景点:")
for area in recommended_areas:
    print(f"景区名称: {area['景区名称']}, 相似度得分: {area['相似度得分']:.2f}, 聚类标签: {area['聚类标签']}")
    print(f"主题1关键词: {area['主题1关键词']}")
    print(f"主题2关键词: {area['主题2关键词']}\n")

mp_white_base = {
    'figure.figsize': (8, 8),
    'figure.dpi': 100,
    'axes.grid': True,
    'axes.labelpad': 14,
    'axes.titlepad': 16,
    'axes.titlecolor': '#333333',
    'axes.labelcolor': '#535353',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'ytick.color': '#535353',
    'ytick.direction': "in",
    'xtick.color': '#535353',
    'xtick.direction': "in",
    'grid.linewidth': 1,
    "grid.alpha": 0.25,
    'lines.linewidth': 1,
    'lines.markersize': 2,
    'text.color': "535353",
    'legend.edgecolor': 'w',
    'scatter.edgecolors': 'w',
    'patch.force_edgecolor': True,
    'patch.edgecolor': 'white',
    'patch.linewidth': 0.6,
    'boxplot.capprops.color': '#535353',
    'boxplot.boxprops.color': 'white',
    'boxplot.boxprops.linewidth': 0.6,
    'boxplot.whiskerprops.color': '#535353',
    'boxplot.whiskerprops.linewidth': 0.6,
    'boxplot.whiskerprops.linestyle': ':',
    'boxplot.medianprops.color': 'white',
    'boxplot.meanprops.color': 'white',
    'boxplot.meanprops.markeredgecolor': 'white',
    'boxplot.meanprops.markerfacecolor': 'white',
}  # 白底风格
""" 绘图风格包 """
from matplotlib import cycler
def mp_white_light():
    """ 白底 清新配色 """
    style = mp_white_base.copy()
    style['axes.prop_cycle'] = cycler('color', ['fb9489', 'a9ddd4', '9ec3db', 'cbc7de', 'fdfcc9'])
    return style


# 绘制柱状图
def plot_recommendations(recommended_areas):
    names = [area['景区名称'] for area in recommended_areas]
    scores = [area['相似度得分'] for area in recommended_areas]

    plt.figure(figsize=(10, 6))
    plt.style.use(mp_white_light())
    plt.barh(names, scores, color='skyblue')
    plt.xlabel('相似度得分')
    plt.title(f'推荐景点 关键词{user_keywords}')
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签SimHei
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    plt.gca().invert_yaxis()  # 使排名从上至下
    plt.tight_layout()
    plt.show()

# 在推荐后调用绘图函数
plot_recommendations(recommended_areas)