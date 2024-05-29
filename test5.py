import json
import time
from pyproj import Proj, Transformer
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
from scipy.interpolate import griddata
from get_sun_direction import calculate_sunray_direction_vector
from embree import cal_intensity
from tqdm import tqdm
from split_tiles import split_and_load_subregions
from sample_points_process import sample_points_from_obj
def points_process(latlon_list,num_samples,mode):
    def generate_dense_points_3d(latlon_list, num_samples):
        # 将列表转换为numpy数组
        # 将列表转换为numpy数组
        points = np.array(latlon_list)

        # 提取经度、纬度和高度
        lats = points[:, 0]
        lons = points[:, 1]
        heights = points[:, 2]

        # 使用Delaunay三角剖分
        delaunay = Delaunay(points[:, :2])

        # 获取点的边界
        min_lat, min_lon, min_height = points.min(axis=0)
        max_lat, max_lon, max_height = points.max(axis=0)

        # 在边界内生成随机的经纬度点
        random_lats = np.random.uniform(min_lat, max_lat, num_samples)
        random_lons = np.random.uniform(min_lon, max_lon, num_samples)
        random_heights = np.random.uniform(min_height, max_height, num_samples)
        random_points = np.vstack((random_lats, random_lons)).T

        # 使用griddata进行插值
        dense_heights = griddata(points[:, :2], points[:, 2], random_points, method='linear')

        # 组合密集点的经纬度和插值的高度
        dense_points = np.column_stack((random_points[:, 0], random_points[:, 1], dense_heights))

        return dense_points

    def generate_dense_points(latlon_list, num_samples):
        # 将列表转换为numpy数组
        points = np.array(latlon_list)

        # 使用Delaunay三角剖分
        delaunay = Delaunay(points)

        # 获取点的边界
        min_lat, min_lon = points.min(axis=0)
        max_lat, max_lon = points.max(axis=0)

        # 在边界内生成随机的经纬度点
        random_lats = np.random.uniform(min_lat, max_lat, num_samples)
        random_lons = np.random.uniform(min_lon, max_lon, num_samples)
        random_points = np.vstack((random_lats, random_lons)).T

        # 使用griddata进行插值
        dense_points = griddata(points, points, random_points, method='linear')

        # 过滤掉插值失败的点
        dense_points = dense_points[~np.isnan(dense_points).any(axis=1)]

        return dense_points


# 示例使用
# latlon_list = [
#     [37.7749, -122.4194],
#     [34.0522, -118.2437],
#     [40.7128, -74.0060],
#     [47.6062, -122.3321]
# ]
# num_samples = 100
    if mode==2:
        dense_points = generate_dense_points(latlon_list, num_samples)

        # 可视化
        plt.figure(figsize=(10, 6))

        # 原始点
        original_points = np.array(latlon_list)
        plt.scatter(original_points[:, 1], original_points[:, 0], c='red', label='Original Points')

        # 生成的密集点
        plt.scatter(dense_points[:, 1], dense_points[:, 0], c='blue', s=10, label='Dense Points')

        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title('Original and Dense Points')
        plt.legend()
        plt.show()
    else:
        dense_points = generate_dense_points_3d(latlon_list, num_samples)
        return dense_points
        # # 可视化
        # fig = plt.figure(figsize=(10, 6))
        # ax = fig.add_subplot(111, projection='3d')
        #
        # # 原始点
        # original_points = np.array(latlon_list)
        # ax.scatter(original_points[:, 1], original_points[:, 0], original_points[:, 2], c='red',
        #            label='Original Points')
        #
        # # 生成的密集点
        # ax.scatter(dense_points[:, 1], dense_points[:, 0], dense_points[:, 2], c='blue', s=10, label='Dense Points')
        #
        # ax.set_xlabel('Longitude')
        # ax.set_ylabel('Latitude')
        # ax.set_zlabel('Height')
        # ax.set_title('Original and Dense Points')
        # ax.legend()
        # plt.show()
def save_to_jsonl(points, filename):
    with open(filename, 'w') as file:
        for point in points:
            json.dump({"latitude": point[0], "longitude": point[1], "height": point[2]}, file)
            file.write('\n')
points = []
with open('list_file.jsonl', 'r') as file:
        for line in file:
            point = json.loads(line)
            points.append([point["latitude"], point["longitude"], point["height"]])
def read_obj_file(obj_file_path):
    vertices = []
    faces = []
    with open(obj_file_path, 'r') as file:
        for line in file:
            if line.startswith('v '):
                parts = line.split()
                vertices.append((float(parts[1]), float(parts[2]), float(parts[3])))
            elif line.startswith('f '):
                parts = line.split()
                faces.append(tuple(int(part.split('/')[0]) - 1 for part in parts[1:]))  # -1 to zero-index
    return vertices, faces


def utm_transform(utm_coordinates):
    # 定义UTM坐标的投影
    utm_proj = Proj(proj='utm', zone=32, ellps='WGS84', south=False)
    # 定义地理坐标（经纬度）的投影
    geo_proj = Proj(proj='latlong', datum='WGS84')

    # 创建 Transformer 对象
    transformer = Transformer.from_proj(utm_proj, geo_proj)

    # 转换为经纬度
    latlong_coordinates = [(transformer.transform(x, y)[1], transformer.transform(x, y)[0], z) for x, y, z in
                           utm_coordinates]

    return latlong_coordinates
vertices, faces= read_obj_file('Munich_center_9_tiles.obj')
dense_points =utm_transform( sample_points_from_obj(vertices, faces, 100))
print(dense_points[:100])
dense_points = points_process(points, 100, 3)
print(dense_points[:100])