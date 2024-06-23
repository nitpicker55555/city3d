import trimesh
import numpy as np
from scipy.spatial import cKDTree
import pandas as pd
from pyproj import Transformer
from read_height import get_height_by_lon_lat
from pyproj import Proj, transform
from pyproj import CRS, Transformer
df = pd.read_csv(r"munich_trans_facade_samples.csv")
df['Floor'] = df['Floor'] * 2.4
# 用列的均值替换NaN值
def convert_epsg25832_to_epsg4326(lon, lat):
    # 创建坐标参考系统
    crs_src = CRS("EPSG:25832")
    crs_dst = CRS("EPSG:4326")

    # 创建转换器
    transformer = Transformer.from_crs(crs_src, crs_dst, always_xy=True)

    # 进行坐标转换
    lon_converted, lat_converted = transformer.transform(lon, lat)
    return lon_converted, lat_converted


selected_columns = df[['join_xcoor', 'join_ycoor', 'Floor']]
line_list_data=selected_columns.values.tolist()
# 定义 EPSG:25832 坐标系

# 转换函数
def transform_coordinates(points, src_proj, dst_proj):
    transformed_points = np.array([transform(src_proj, dst_proj, x, y) for x, y in points])
    return transformed_points

# 示例 EPSG:25832 点坐标
epsg25832_points =   np.array(line_list_data[1000:2000])
obj_mesh = trimesh.load(r'Munich_center_9_tiles.obj')
obj_vertices = obj_mesh.vertices
obj_faces = obj_mesh.faces
tree = cKDTree(obj_vertices)
# 将 EPSG:25832 坐标转换为 WGS84 坐标
# transformed_points = transform_coordinates(epsg25832_points, epsg25832, wgs84)
colors = np.array([[255, 0, 0, 255] for _ in range(len(epsg25832_points))])  # RGBA 格式

projected_points = np.zeros_like(epsg25832_points)
points_list=[]
# 遍历所有点，计算每个点的最近表面点
for i, point in enumerate(epsg25832_points):
    # closest_point, distance, triangle_id = obj_mesh.nearest.on_surface([point])

    point[2] = get_height_by_lon_lat(convert_epsg25832_to_epsg4326(point[0], point[1]))
    points_list.append(point[2])
    projected_points[i] = point # 获取返回的最近点坐标

    # distances = np.linalg.norm(obj_vertices - point, axis=1)

    # 找出最近的距离
    # min_distance = np.min(distances)

    # print("最近的距离是:", min_distance)
# print(points_list)
# 创建点云
point_cloud = trimesh.points.PointCloud(projected_points, colors=colors)

# 加载 OBJ 文件


#SELECT height FROM locations
# ORDER BY geom <-> ST_SetSRID(ST_Point(你的经度, 你的纬度), 4326)
# LIMIT 1;



# 创建场景
scene = trimesh.Scene()
scene.add_geometry(point_cloud)
scene.add_geometry(obj_mesh)

# 显示场景
scene.show()