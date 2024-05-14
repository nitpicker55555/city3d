import trimesh
import numpy as np
from pyproj import Transformer

# 输入和输出文件路径
input_file = r"q.obj"
output_file = "q2.obj"

# 创建坐标变换对象
transformer = Transformer.from_crs("epsg:25832", "epsg:4326", always_xy=True)

# 读取OBJ文件
mesh = trimesh.load_mesh(input_file)

# 假设顶点坐标存储在mesh.vertices中
vertices = mesh.vertices

# 转换顶点坐标
transformed_vertices = []
for vertex in vertices:
    x, y, z = vertex
    lon, lat = transformer.transform(x, y)
    transformed_vertices.append([lon, lat, z])

transformed_vertices = np.array(transformed_vertices)

# 创建新的网格对象
transformed_mesh = trimesh.Trimesh(vertices=transformed_vertices, faces=mesh.faces)

# 保存转换后的OBJ文件
transformed_mesh.export(output_file)

print(f"Transformation complete. Saved to {output_file}")
