import trimesh
import numpy as np
from scipy.spatial import cKDTree

def latlon_to_xyz(lat, lon, radius=6378137):
    """
    将经纬度转换为三维空间中的坐标。
    :param lat: 纬度
    :param lon: 经度
    :param radius: 地球半径，默认为 WGS84 标准的半径（6378137 米）
    :return: (x, y, z) 坐标
    """
    lat = np.deg2rad(lat)
    lon = np.deg2rad(lon)
    x = radius * np.cos(lat) * np.cos(lon)
    y = radius * np.cos(lat) * np.sin(lon)
    z = radius * np.sin(lat)
    return np.array([x, y, z])

def find_lowest_height(mesh, point):
    """
    找到模型中距离给定点最近的最低高度。
    :param mesh: 三维模型的 trimesh 对象
    :param point: 给定的 (x, y, z) 点
    :return: 最低高度
    """
    kdtree = cKDTree(mesh.vertices)
    dist, idx = kdtree.query(point)
    nearest_vertices = mesh.vertices[idx]
    lowest_height = nearest_vertices[:, 2].min()
    return lowest_height

def get_lowest_height_at_latlon(mesh,point):
    """
    输入经纬度，输出该点在 .obj 模型中的最低高度。
    :param obj_path: .obj 文件路径
    :param lat: 纬度
    :param lon: 经度
    :return: 最低高度
    """
    # mesh = trimesh.load(obj_path)
    # point = latlon_to_xyz(lat, lon)
    lowest_height = find_lowest_height(mesh, point)
    return lowest_height

# # 示例使用
# obj_file_path = 'path_to_your_obj_file.obj'
# latitude = 40.7128  # 示例纬度
# longitude = -74.0060  # 示例经度
#
# lowest_height = get_lowest_height_at_latlon(obj_file_path, latitude, longitude)
# print(f'The lowest height at the given latitude and longitude is: {lowest_height}')
