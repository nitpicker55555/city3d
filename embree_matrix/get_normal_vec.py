import numpy as np
import trimesh

# 加载Mesh模型
mesh = trimesh.load_mesh(r"path_to_save_mesh.ply")

# 确保顶点顺序一致并法向外指
if not mesh.is_winding_consistent:
    mesh.fix_normals()

# 加载三角形ID
triangle_ids = np.load('triangle_id.npy')

# 提取指定三角形的顶点索引
triangles = mesh.faces[triangle_ids]

normals = np.cross(mesh.vertices[triangles[:, 1]] - mesh.vertices[triangles[:, 0]],
                   mesh.vertices[triangles[:, 2]] - mesh.vertices[triangles[:, 0]])

# 计算每个向量的长度
norms = np.linalg.norm(normals, axis=1)

# 避免除以零的情况，对于长度为0的向量使用(1, 0, 0)代替（或任何合适的默认向量）
normals[norms == 0] = [0, 0, -1]
norms[norms == 0] = 1  # 防止下面的除法操作出现除以零

# 归一化法向量
normals = normals / norms[:, np.newaxis]
# 保存法向量到npy文件
np.save('saved_normals.npy', normals)
