import psycopg2
import time
def connect_to_db(dbname, user, password, host, port):
    try:
        # 连接到PostgreSQL数据库
        connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        print("Connection to PostgreSQL DB successful")
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        return None

def get_height_by_lon_lat( lon_lat):
    try:


        # 定义查询语句
        query = """
SELECT height FROM locations
ORDER BY geom <-> ST_SetSRID(ST_Point(%s, %s), 4326)
LIMIT 1;
        """

        # 执行查询
        cursor.execute(query, (lon_lat[0],lon_lat[1]))
        result = cursor.fetchone()

        if result:
            # print(f"Height: {result[0]}")
            return result[0]
        else:
            print(lon_lat)
            return 523

    except (Exception, psycopg2.Error) as error:
        print("Error while querying PostgreSQL", error)
        cursor.execute("ROLLBACK;")
        cursor.execute("SET statement_timeout = 3000;")  # 设置3秒超时
        return 522

# 使用示例
connection = connect_to_db(
    dbname="munich_height",
    user="postgres",
    password="9417941",
    host="localhost",
    port="5432"
)
cursor = connection.cursor()
cursor.execute("SET statement_timeout = 3000;")  # 设置3秒超时
# if connection:
#     while True:
#         lon_lat=input(":")
#         start_time=time.time()
#         height = get_height_by_lon_lat(connection, lon_lat)
#         total_time=time.time()-start_time
#         print(total_time)
#     # 关闭数据库连接
#     # connection.close()
#     #     print("PostgreSQL connection is closed")
