import pandas as pd 
import pyarrow as pa 
import pyarrow.parquet as pq

# 定义读取CSV文件的块大小
chunksize = 10**6  # 每次读取100万行

csv_file = 'data.csv'
parquet_file = 'large_file.parquet'

# 使用pandas逐块读取CSV文件
reader = pd.read_csv(csv_file, chunksize=chunksize)

# 读取第一块数据以确定schema
first_chunk = next(reader)
table = pa.Table.from_pandas(first_chunk)

# 打开一个新的Parquet文件以写入，并设置schema
with pq.ParquetWriter(parquet_file, table.schema) as writer:
    writer.write_table(table)
    
    # 继续处理剩余的块
    for i, chunk in enumerate(reader, start=1):
        print(f'Processing chunk {i}...')
        table = pa.Table.from_pandas(chunk)
        writer.write_table(table)

print('CSV to Parquet conversion completed.')
