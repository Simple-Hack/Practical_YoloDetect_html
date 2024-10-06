import pandas as pd
import jieba
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from collections import Counter
import re
# 加载数据
data = pd.read_csv(r"D:\qq\2385786690\FileRecv\啊_comment.csv")

# 自定义停用词列表，这里添加了一些语气词
# custom_stopwords = set(STOPWORDS)
# custom_stopwords.update(["的", "是", "我", "在", "了", "就", "也", "很", "和", "还", "不", "有", "很", "但", "与", "来", "去", "到",
#                          "都", "还是", "全部", "很多", "可以", "呢", "啦", "吧", "哟", "哦", "呀", "啊", "呢",'你','好','不错','这里','我们','就是','一个','没有','非常'])

def load_stopwords(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        stopwords = set(word.strip() for word in file.readlines())
    return stopwords
stop_words = load_stopwords('baidu_stopwords.txt')
# 定义一个函数来处理文本
def preprocess_text(text):
    text = str(text)
    
    # 移除数字、特殊符号和英文字符
    text = re.sub(r'[^一-龥\s]', '', text)  # 移除非中文字符
    # 分词
    seg_list = jieba.cut(text)
    # 过滤停用词
    filtered_words = [word for word in seg_list if word not in stop_words]
    return " ".join(filtered_words)

# 将评论标题和评论内容合并
data['combined_text'] = data['用户评论']

# 应用预处理函数
data['processed_content'] = data['combined_text'].apply(preprocess_text)

# 合并所有评论为一个长字符串
all_text = ' '.join(data['processed_content'])

# 统计词频
word_counts = Counter(all_text.split())

# 生成词云
wc = WordCloud(font_path='simhei.ttf',  # 字体文件路径，确保支持中文
               background_color='white',
               width=800,
               height=600).generate_from_frequencies(word_counts)

# 显示词云
plt.figure(figsize=(10, 8))
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
plt.show()