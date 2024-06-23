import pycuda.autoinit
import pycuda.driver as cuda
from pycuda.compiler import SourceModule
import numpy as np
import trimesh
from get_sun_direction import calculate_sunray_direction_vector
# 定义用于计算光照强度的余弦函数

import trimesh
import numpy as np
from scipy.spatial import cKDTree
import pandas as pd
from pyproj import Transformer
from tqdm import tqdm
from pyproj import Proj, transform
from get_sun_direction import calculate_sunray_direction_vector
df = pd.read_csv(r"munich_trans_facade_samples.csv")
df['Floor'] = df['Floor'] * 2.4 + 522.5
# 用列的均值替换NaN值
from trimesh.visual.color import ColorVisuals
scene = trimesh.Scene()

selected_columns = df[['join_xcoor', 'join_ycoor', 'Floor']]
line_list_data=selected_columns.values.tolist()
def cosin_cal(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

# 加载网格
obj_mesh = trimesh.load('q.obj')
epsg25832_points =   np.array(line_list_data[2800:2801])
# 计算面法线
face_normals = obj_mesh.face_normals

# 定义一个点
point = epsg25832_points[0]
date_str = '2024-05-14'
time_str = '12:50'
sun_vec = calculate_sunray_direction_vector(date_str, time_str)

# 最近点计算
closest_point, distance, triangle_id = obj_mesh.nearest.on_surface([point])
intersection_normals = face_normals[triangle_id]

# 设置光线方向


# CUDA内核代码
mod = SourceModule("""
__global__ void ray_intersect(
    float3 *ray_origins, float3 *ray_directions, 
    float3 *hit_points, int *hit_ids,
    float3 *vertices, int3 *faces, int num_faces)
{
    int idx = threadIdx.x + blockDim.x * blockIdx.x;
    if (idx >= num_faces) return;

    // 从全局内存读取数据
    float3 origin = ray_origins[0];
    float3 direction = ray_directions[0];
    float3 v0 = vertices[faces[idx].x];
    float3 v1 = vertices[faces[idx].y];
    float3 v2 = vertices[faces[idx].z];

    // 计算相交（简化版的Möller–Trumbore算法）
    float3 edge1 = v1 - v0;
    float3 edge2 = v2 - v0;
    float3 h = cross(direction, edge2);
    float a = dot(edge1, h);
    if (a > -0.00001 && a < 0.00001) return; // 平行光线

    float f = 1.0 / a;
    float3 s = origin - v0;
    float u = f * dot(s, h);
    if (u < 0.0 || u > 1.0) return;

    float3 q = cross(s, edge1);
    float v = f * dot(direction, q);
    if (v < 0.0 || u + v > 1.0) return;

    float t = f * dot(edge2, q);
    if (t > 0.00001) { // 相交
        hit_points[idx] = origin + t * direction;
        hit_ids[idx] = idx;
    }
}
""")

# 准备数据
vertices = np.array(obj_mesh.vertices, dtype=np.float32)
faces = np.array(obj_mesh.faces, dtype=np.int32)
ray_origins = np.array([closest_point[0]], dtype=np.float32)
ray_directions = np.array([sun_vec], dtype=np.float32)
hit_points = np.zeros((len(faces), 3), dtype=np.float32)
hit_ids = np.full((len(faces)), -1, dtype=np.int32)

# 分配设备内存
d_vertices = cuda.mem_alloc(vertices.nbytes)
d_faces = cuda.mem_alloc(faces.nbytes)
d_ray_origins = cuda.mem_alloc(ray_origins.nbytes)
d_ray_directions = cuda.mem_alloc(ray_directions.nbytes)
d_hit_points = cuda.mem_alloc(hit_points.nbytes)
d_hit_ids = cuda.mem_alloc(hit_ids.nbytes)

# 复制数据到设备
cuda.memcpy_htod(d_vertices, vertices)
cuda.memcpy_htod(d_faces, faces)
cuda.memcpy_htod(d_ray_origins, ray_origins)
cuda.memcpy_htod(d_ray_directions, ray_directions)
cuda.memcpy_htod(d_hit_points, hit_points)
cuda.memcpy_htod(d_hit_ids, hit_ids)

# 启动CUDA内核
ray_intersect = mod.get_function("ray_intersect")
num_faces = np.int32(len(faces))
block_size = 256
grid_size = int(np.ceil(len(faces) / block_size))
ray_intersect(d_ray_origins, d_ray_directions, d_hit_points, d_hit_ids, d_vertices, d_faces, num_faces, block=(block_size, 1, 1), grid=(grid_size, 1))

# 复制结果回主机
cuda.memcpy_dtoh(hit_points, d_hit_points)
cuda.memcpy_dtoh(hit_ids, d_hit_ids)

# 获取光线追踪结果
locations = hit_points[hit_ids >= 0]
index_ray = np.where(hit_ids >= 0)[0]
index_tri = hit_ids[hit_ids >= 0]

# 判断光线是否与网格相交
if len(locations) > 0:
    light_intensity = 0
else:
    light_intensity = cosin_cal(intersection_normals[0], sun_vec)
    if light_intensity < 0:
        light_intensity = 0

print("Light intensity:", light_intensity)
