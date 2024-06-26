import json
from datetime import datetime, timedelta
import trimesh
import concurrent.futures
import numpy as np
from scipy.spatial import cKDTree
import pandas as pd
from pyproj import Transformer
from read_height import get_height_by_lon_lat
from pyproj import CRS, Transformer

from tqdm import tqdm
from pyproj import Proj, transform
from get_sun_direction import calculate_sunray_direction_vector
df = pd.read_csv(r"munich_trans_facade_samples.csv")
df['Floor'] = df['Floor'] * 2.4
# 用列的均值替换NaN值
from trimesh.visual.color import ColorVisuals
scene = trimesh.Scene()
def convert_epsg25832_to_epsg4326(lon, lat):
    # 创建坐标参考系统
    crs_src = CRS("EPSG:25832")
    crs_dst = CRS("EPSG:4326")

    # 创建转换器
    transformer = Transformer.from_crs(crs_src, crs_dst, always_xy=True)

    # 进行坐标转换
    lon_converted, lat_converted = transformer.transform(lon, lat)
    return lon_converted, lat_converted

def visualize_ray_with_gradient(scene,start_point, direction, length, intensity):
    """
    绘制一个从黑到红的渐变射线，颜色强度由输入的小数决定。

    参数:
        start_point (numpy.array): 射线的起始点。
        direction (numpy.array): 射线的方向向量。
        length (float): 射线的长度。
        intensity (float): 颜色的强度，0到1之间的小数，决定红色的饱和度。
    """
    # 验证输入值是否在0到1之间
    if not (0 <= intensity <= 1):
        raise ValueError("Intensity must be a float between 0 and 1.")

    # 计算颜色
    red_value = int(255 * intensity)  # 将强度映射到0-255之间
    color = [red_value, 0, 0, 255]    # 创建 RGBA 颜色值

    # 创建路径
    ray_path = np.hstack((start_point, start_point + direction * length)).reshape(-1, 2, 3)

    # 使用 trimesh 加载路径
    ray_visualize = trimesh.load_path(ray_path)

    # 获取顶点数量
    vertex_count = ray_visualize.vertices.shape[0]

    # 为每个顶点创建一个颜色数组
    vertex_colors = np.tile(color, (vertex_count, 1))

    # 为射线设置颜色
    ray_visualize.visual = ColorVisuals(vertex_colors=vertex_colors)

    # 将射线添加到场景中
    scene.add_geometry(ray_visualize)
    # return ray_visualize


selected_columns = df[['join_xcoor', 'join_ycoor', 'Floor']]
line_list_data=selected_columns.values.tolist()


def transform_coordinates(points, src_proj, dst_proj):
    transformed_points = np.array([transform(src_proj, dst_proj, x, y) for x, y in points])
    return transformed_points
def cosin_cal(vector1,vector2):
    dot_product = np.dot(vector1, vector2)

    # 计算两个向量的模
    norm1 = np.linalg.norm(vector1)
    norm2 = np.linalg.norm(vector2)

    # 计算余弦值
    cosine_angle = dot_product / (norm1 * norm2)
    return cosine_angle
def judge_intersection(origin,direction):
    locations, index_ray, index_tri = obj_mesh.ray.intersects_location(
        ray_origins=[origin],
        ray_directions=[direction]
    )

    # 检查是否有交点
    return len(locations) > 0
# 示例 EPSG:25832 点坐标
epsg25832_points =   np.array(line_list_data[2800:2801])
obj_mesh = trimesh.load(r'q.obj')

face_normals = obj_mesh.face_normals
# obj_vertices = obj_mesh.vertices
# obj_faces = obj_mesh.faces
# tree = cKDTree(obj_vertices)
# 将 EPSG:25832 坐标转换为 WGS84 坐标
# transformed_points = transform_coordinates(epsg25832_points, epsg25832, wgs84)
# colors = np.array([[255, 0, 0, 255] for _ in range(len(epsg25832_points))])  # RGBA 格式

# projected_points = np.zeros_like(epsg25832_points)
sun_intensity= {}
# 遍历所有点，计算每个点的最近表面点

date_list = ['2024-06-20','2024-12-21']
# time_str = '12:50'
time_list={'2024-06-20':["05:15","21:45"],'2024-12-21':["08:30","16:00"]}
ray_list=[]


def process_point(index_point):
    i, point = index_point
    point[2] += get_height_by_lon_lat(convert_epsg25832_to_epsg4326(point[0], point[1]))

    closest_point, distance, triangle_id = obj_mesh.nearest.on_surface([point])
    intersection_normals = face_normals[triangle_id]
    locations, index_ray, index_tri = obj_mesh.ray.intersects_location(
        ray_origins=[closest_point[0]],
        ray_directions=[sun_vec]
    )

    if len(locations)>0:
        light_intensity = 0
    else:
        light_intensity = cosin_cal(intersection_normals[0], sun_vec)
        if light_intensity < 0:
            light_intensity = 0

    # 返回处理好的数据，以便之后统一写入文件
    return {'index': i, 'time': time_str, 'date': date_str, 'light_intensity': light_intensity}


for date_str in date_list:


    # 起始时间
    start_time = datetime.strptime(time_list[date_str][0], "%H:%M")
    # 结束时间
    end_time = datetime.strptime(time_list[date_str][1], "%H:%M")
    # 时间增量
    time_step = timedelta(minutes=30)

    # 循环从 start_time 到 end_time，每次增加 time_step
    current_time = start_time
    while current_time <= end_time:

                time_str=current_time
                sun_vec = calculate_sunray_direction_vector(date_str, time_str)
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    # 使用tqdm显示进度条
                    results = list(
                        tqdm(executor.map(process_point, enumerate(epsg25832_points)), total=len(epsg25832_points)))

                # 将结果写入文件
                with open('sun_intensity.jsonl', 'a') as file:
                    for result in results:
                        file.write(json.dumps(result) + '\n')
                current_time += time_step


# point_cloud = trimesh.points.PointCloud(projected_points, colors=colors)
#
#
# # 创建场景
# # scene = trimesh.Scene()
#
#
# scene.add_geometry(point_cloud)
# scene.add_geometry(obj_mesh)
# # 显示场景
# scene.show()