import trimesh
import numpy as np
from scipy.spatial import cKDTree
import pandas as pd
from pyproj import Transformer
# from read_height import get_height_by_lon_lat
from pyproj import Proj, transform



# 示例 EPSG:25832 点坐标
epsg25832_points =   np.load(r"closest_point.npy")
obj_mesh = trimesh.load(r"path_to_save_mesh.ply")
obj_vertices = obj_mesh.vertices
obj_faces = obj_mesh.faces
tree = cKDTree(obj_vertices)

num_points = len(epsg25832_points)
colors = np.full((num_points, 4), [255, 0, 0, 255])
# 创建点云
point_cloud = trimesh.points.PointCloud(epsg25832_points, colors=colors)

# 创建场景
scene = trimesh.Scene()
scene.add_geometry(point_cloud)
scene.add_geometry(obj_mesh)

# 显示场景
scene.show()