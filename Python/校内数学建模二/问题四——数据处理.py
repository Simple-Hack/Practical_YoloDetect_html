import pandas as pd
import numpy as np

# 文件路径
file_path = r"D:\数学建模\题目\B题\附件.xlsx"

# 读取数据
data = pd.read_excel(file_path)

# 提取数据并进行单位转换
z_values = data.iloc[1:253, 2:204].values  # 转换为米

# 创建新的坐标系统
x_values = np.arange(0.00, 4.01, 0.02).tolist()
y_values = np.arange(0.00, 5.01, 0.02).tolist()

# 将转换后的数据写入新文件
output_file_path = "111111.csv"
with open(output_file_path, 'w') as f:
    # 写入表头
    f.write("x,y,z\n")
    
    # 写入数据
    for y in y_values:
        for i, x in enumerate(x_values):
            z = z_values[y_values.index(y)][i]
            f.write(f"{x:.2f},{y:.2f},{z:.2f}\n")

print("Data has been written to the file.")