import pandas as pd
import random

# 加载 CSV 文件
result_df = pd.read_csv('scenic_area_topics_with_clusters.csv')

# 将主题关键词列从字符串转换为列表
result_df['主题1关键词'] = result_df['主题1关键词'].apply(lambda x: eval(x))
result_df['主题2关键词'] = result_df['主题2关键词'].apply(lambda x: eval(x))

# 随机选取三个景区
random_scenic_areas = result_df.sample(n=3)

# 输出这些景区的信息
print(random_scenic_areas[['景区名称', '主题1关键词', '主题2关键词']])