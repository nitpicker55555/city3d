import json

import trimesh
import numpy as np
from scipy.spatial import cKDTree
import pandas as pd
from pyproj import Transformer
from tqdm import tqdm
from pyproj import Proj, transform
from get_sun_direction import calculate_sunray_direction_vector
df = pd.read_csv(r"munich_trans_facade_samples.csv")
df['Floor'] = df['Floor'] * 2.4
from read_height import get_height_by_lon_lat
# 用列的均值替换NaN值
from trimesh.visual.color import ColorVisuals
scene = trimesh.Scene()

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
# 定义 EPSG:25832 坐标系

# 转换函数
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
epsg25832_points =   np.array(line_list_data)
print('load finish')
obj_mesh = trimesh.load(r"C:\Users\TUM_LfK\Documents\Python Scripts\combined_mesh.obj")
print('load finish')

face_normals = obj_mesh.face_normals
print('load finish')

# obj_vertices = obj_mesh.vertices
# obj_faces = obj_mesh.faces
# tree = cKDTree(obj_vertices)
# 将 EPSG:25832 坐标转换为 WGS84 坐标
# transformed_points = transform_coordinates(epsg25832_points, epsg25832, wgs84)
# colors = np.array([[255, 0, 0, 255] for _ in range(len(epsg25832_points))])  # RGBA 格式

# projected_points = np.zeros_like(epsg25832_points)
# sun_intensity= {}
# 遍历所有点，计算每个点的最近表面点

date_list = ['2024-06-20','2024-12-21']
# time_str = '12:50'
# ray_list=[]
for date_str in date_list:
        for hour in range(24):  # 循环从0到23小时
            for minute in range(0, 60, 15):  # 每小时的分钟数从0开始，以15为步长
                time_str=f'{hour:02}:{minute:02}'
                sun_vec = calculate_sunray_direction_vector(date_str, time_str)
                for i, point in tqdm( enumerate(epsg25832_points)):
                    closest_point, distance, triangle_id = obj_mesh.nearest.on_surface([point])
                    # projected_points= closest_point[0]  # 获取返回的最近点坐标
                    intersection_normals = face_normals[triangle_id]
                    intersects=judge_intersection(closest_point[0],sun_vec)
                    if intersects:
                        light_intensity=0
                    else:
                        light_intensity=cosin_cal(intersection_normals[0], sun_vec)
                        if light_intensity<0:
                            light_intensity=0
                    with open('sun_intensity.jsonl','a')as file:
                            file.write(json.dumps({'index':i,'time':time_str,'date':date_str,'light_intensity':light_intensity}))

# point_cloud = trimesh.points.PointCloud(projected_points, colors=colors)


# 创建场景
# scene = trimesh.Scene()


# scene.add_geometry(point_cloud)
# scene.add_geometry(obj_mesh)
# 显示场景
# scene.show()