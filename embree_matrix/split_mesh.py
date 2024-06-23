import trimesh
import numpy as np
import numpy as np
from scipy.spatial import cKDTree
import time
starts_time=time.time()
mesh = trimesh.load(r'C:\Users\TUM_LfK\Documents\Python Scripts\combined_mesh.obj')
print(time.time()-starts_time)
longitude_bounds = (np.min(mesh.vertices[:, 0]), np.max(mesh.vertices[:, 0]))
latitude_bounds = (np.min(mesh.vertices[:, 1]), np.max(mesh.vertices[:, 1]))
longitude_bounds = (673987.121, 704010.776)
latitude_bounds = (5325983.72, 5348001.731)
# print(longitude_bounds,latitude_bounds)
latitude_divisions = 10
longitude_divisions = 11
#
# # 计算网格步长
lat_step = (latitude_bounds[1] - latitude_bounds[0]) / latitude_divisions
lon_step = (longitude_bounds[1] - longitude_bounds[0]) / longitude_divisions
#
# # 创建空的网格列表，用于存储每个区域的顶点索引
vertex_groups = [[[] for _ in range(longitude_divisions)] for _ in range(latitude_divisions)]

# 分配顶点到相应的区域
for i, vertex in enumerate(mesh.vertices):
    lat_idx = int((vertex[1] - latitude_bounds[0]) / lat_step)
    lon_idx = int((vertex[0] - longitude_bounds[0]) / lon_step)
    lat_idx = min(lat_idx, latitude_divisions - 1)
    lon_idx = min(lon_idx, longitude_divisions - 1)
    vertex_groups[lat_idx][lon_idx].append(i)

# 根据顶点索引，创建每个区域的mesh
mesh_grid = [[None for _ in range(longitude_divisions)] for _ in range(latitude_divisions)]
for lat_idx in range(latitude_divisions):
    for lon_idx in range(longitude_divisions):
        # 找出当前区域的所有顶点索引
        indices = vertex_groups[lat_idx][lon_idx]
        # 创建子网格
        if indices:
            submesh = mesh.submesh([indices], append=True)
            mesh_grid[lat_idx][lon_idx] = submesh
def find_mesh_by_coords(longitude,latitude):
    lat_idx = int((latitude - latitude_bounds[0]) / lat_step)
    lon_idx = int((longitude - longitude_bounds[0]) / lon_step)
    lat_idx = min(max(lat_idx, 0), latitude_divisions - 1)
    lon_idx = min(max(lon_idx, 0), longitude_divisions - 1)
    # return mesh_grid[lat_idx][lon_idx]
    return lat_idx,lon_idx
