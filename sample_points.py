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
# data_without_height=[]
# for i in points:
#     data_without_height.append([i[0],i[1]])
date_str = '2024-05-14'
time_str = '17:00'
sun_vec=calculate_sunray_direction_vector(date_str,time_str)

# dense_points=points_process(points,20000,3)
# intensity_list = cal_intensity(sun_vec, dense_points)

obj_list={'q.obj':'16 MB','Munich_center_2_tiles.obj':"40 MB",'Munich_center_9_tiles.obj':"131 MB"}
def benchmark_intensity(obj,split_time,vertices, faces,index,start=8000, end=80000, step=2000):
    times = []
    sizes = list(range(start, end + 1, step))

    for size in tqdm(sizes):
        dense_points=(sample_points_from_obj(vertices, faces, size))
        # print(dense_points[:100])
        # dense_points = points_process(points, size, 3)
        # print(dense_points[:100])
        _,time_taken=cal_intensity(sun_vec, dense_points,obj)
        all_time=split_time+time_taken
        # print(time_taken,'cal_intensity',split_time,'split_time',all_time,'all_time')

        # Record the time taken
        times.append(time_taken)
    return times[1:],sizes[1:]
    # Plotting the results
    # plt.figure(figsize=(10, 6))
    # plt.plot(sizes, times, marker='o')
    # plt.xlabel('Number of Points')
    # plt.ylabel('Time (seconds)')
    # plt.title('Time taken by ray mesh intersects for different range of points')
    # plt.grid(True)
    # plt.savefig(f'figure{index}.png')
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
def plot_multiple_lists(x, y_lists, labels=None, title="Multiple Line Plot", xlabel="X-axis", ylabel="Y-axis"):
    """
    Plots multiple y-lists against a single x-list as separate lines on the same plot.

    Parameters:
    x : list
        A single list of x values.
    y_lists : list of lists
        Each sublist contains y values to be plotted against the x values.
    labels : list of str, optional
        Labels for each y-list to be used in the legend.
    title : str, optional
        Title of the plot.
    xlabel : str, optional
        Label for the X-axis.
    ylabel : str, optional
        Label for the Y-axis.
    """
    for i, y in enumerate(y_lists):
        plt.plot(x, y, label=labels[i] if labels else f'Line {i + 1}')

    plt.title(title)
    # plt.xlabel(xlabel)
    # plt.ylabel(ylabel)
    plt.xlabel('Number of Points')
    plt.ylabel('Time (seconds)')
    if labels:
        plt.legend()
    plt.grid(True)
    plt.savefig('figure_multi_time_taken.png')
    plt.show()

vertices, faces= read_obj_file('Munich_center_9_tiles.obj')
split_list=[]
all_result_list=[]
x_labels=[]
labels=[]
for i in range(9):
    split_list.append(i)
    start_time = time.time()
    mesh=split_and_load_subregions(vertices, faces, split_list)
    end_time = time.time()
    times,x_labels=benchmark_intensity(mesh,end_time-start_time,vertices, faces,i)
    labels.append(f"{i+1}")
    all_result_list.append(times)
print(all_result_list)
plot_multiple_lists(x_labels,all_result_list,labels)