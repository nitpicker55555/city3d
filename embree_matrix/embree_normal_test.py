import time
import pandas as pd
df = pd.read_csv(r'munich_trans_facade_samples.csv')

df['Floor'] = df['Floor'] * 2.4 + 502.5
selected_columns = df[['join_xcoor', 'join_ycoor', 'Floor']]
line_list_data=selected_columns.values.tolist()
from get_sun_direction import calculate_sunray_direction_vector
# from embree import cal_intensity
# from data_process import *
# from sample_points_process import sample_points_from_obj

import numpy as np
import trimesh

# load a file by name or from a buffer
mesh = trimesh.load_mesh(r"D:\puzhen\hi_structure\city3d\Munich_center_9_tiles.obj")
start_time = time.time()

from pyproj import Transformer
transformer = Transformer.from_crs("EPSG:4326", "EPSG:25832")
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
def convert(latitude, longitude):
    # print(latitude,longitude)
    return transformer.transform(longitude, latitude)


collect_origins = []
collect_directions = []
date_str = '2024-05-14'
time_str = '11:50'
sun_vec = calculate_sunray_direction_vector(date_str, time_str)
# print(sun_vec)
# vertices, faces=read_obj_file('q.obj')
# list_=cal_intensity(sun_vec,data)
# dense_points = data[:20]

# for i in range(20):
    # print(data[i])

    # collect_origins.append([*convert(data_ori[i][0], data_ori[i][1]), data_ori[i][2]-45])

    # collect_directions.append(sun_vec)
# for each_line in line_list_data:
#     collect_origins.append([each_line[0],each_line[1],each_line[2]*2.4+502])
#     collect_directions.append(sun_vec)
ray_origins = np.array(line_list_data)
ray_directions = np.array([sun_vec]*len(line_list_data))
from embreex import rtcore_scene
# run the mesh- ray query
locations, index_ray, index_tri  = trimesh.ray.ray_pyembree.RayMeshIntersector(mesh).intersects_location(
        ray_origins=ray_origins,
        ray_directions=ray_directions)
# stack rays into line segments for visualization as Path3D
ray_visualize = trimesh.load_path(np.hstack((ray_origins,
                                             ray_origins + ray_directions*200.0)).reshape(-1, 2, 3))
# face_normals = mesh.face_normals

# 根据 index_tri 获取交点所在平面的法线
# intersection_normals = face_normals[index_tri]
points = trimesh.points.PointCloud(locations)
# normals_visualize = trimesh.load_path(np.hstack((locations, locations + intersection_normals*200.0)).reshape(-1, 2, 3))

print(len(collect_origins))
hit_rays = set(index_ray)
all_rays = set(range(len(ray_origins)))
no_hit_rays = all_rays - hit_rays


# 输出结果
print("射线交叉的索引：", len(sorted(list(hit_rays))))
print("射线没有交叉的索引：", len(sorted(list(no_hit_rays))))

## make mesh white- ish
mesh.visual.face_colors = [255,255,255,255]
mesh.visual.face_colors[index_tri] = [255, 0, 0, 255]
end_time = time.time()

total_time = end_time - start_time
# list_=cal_intensity(sun_vec,data_ori)
# 输出时间
print("总计算时间：{:.2f} 秒".format(total_time))
# create a visualization scene with rays, hits, and mesh
scene = trimesh.Scene([ray_visualize, mesh])
scene.show()


# 计算总时间