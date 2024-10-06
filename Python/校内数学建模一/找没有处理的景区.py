import pandas as pd

# 读取包含所有景区名字的Excel文件
excel_file_path = r"D:\qq\2385786690\FileRecv\data11.xlsx"
excel_data = pd.read_excel(excel_file_path)
all_scenic_areas = excel_data['名称'].tolist()

# 读取包含评论数据的CSV文件
csv_file_path = r"D:\VsFile\Python\啊_comment.csv"
csv_data = pd.read_csv(csv_file_path)
commented_scenic_areas = csv_data['景点'].unique().tolist()

# 找出CSV文件中未出现的景区
missing_scenic_areas = list(set(all_scenic_areas) - set(commented_scenic_areas))

# 显示未出现在CSV文件中的景区
print("未出现在CSV文件中的景区:")
for scenic_area in missing_scenic_areas:
    print(scenic_area)