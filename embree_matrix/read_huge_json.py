import json
import psycopg2
from tqdm import tqdm

# 连接到 Postgres 数据库
conn = psycopg2.connect(
        dbname="munich_height",
        user="postgres",
        password="9417941",
        host="localhost",
        port="5432"
)
cur = conn.cursor()

# 逐行读取 JSON 文件
with open('output_data.json', 'r') as f:
    f.readline()  # 跳过开头的 '{'
    for line in tqdm(f):
        line = line.strip().rstrip(',')  # 去除行末的逗号和两端的空格
        if line == '}':  # 如果到达文件末尾的 '}', 终止循环
            break
        # 解析键值对，其中 lon_lat 是 '经度,纬度' 形式的字符串，height 是对应的高度值
        lon_lat, height = line.split(': ')
        lon, lat = map(float, lon_lat.strip('"').split(','))
        height = float(height)

        # 在 SQL 中直接使用 ST_SetSRID 和 ST_Point 函数
        cur.execute(
            "INSERT INTO locations (lat, lon, height, geom) VALUES (%s, %s, %s, ST_SetSRID(ST_Point(%s, %s), 4326))",
            (lat, lon, height, lon, lat)
        )
# 提交事务
conn.commit()

# 关闭连接
cur.close()
conn.close()
