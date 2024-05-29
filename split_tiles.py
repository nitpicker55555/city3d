import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import trimesh




def get_bounds(vertices):
    min_x = min(vertices, key=lambda v: v[0])[0]
    max_x = max(vertices, key=lambda v: v[0])[0]
    min_y = min(vertices, key=lambda v: v[1])[1]
    max_y = max(vertices, key=lambda v: v[1])[1]
    min_z = min(vertices, key=lambda v: v[2])[2]
    max_z = max(vertices, key=lambda v: v[2])[2]
    return (min_x, max_x), (min_y, max_y), (min_z, max_z)

def get_subregion_bounds(x_bounds, y_bounds, z_bounds, index):
    x_min, x_max = x_bounds
    y_min, y_max = y_bounds
    z_min, z_max = z_bounds

    x_third = (x_max - x_min) / 3
    y_third = (y_max - y_min) / 3

    subregion_bounds = [
        (x_min, x_min + x_third, y_min, y_min + y_third, z_min, z_max),
        (x_min + x_third, x_min + 2 * x_third, y_min, y_min + y_third, z_min, z_max),
        (x_min + 2 * x_third, x_max, y_min, y_min + y_third, z_min, z_max),
        (x_min, x_min + x_third, y_min + y_third, y_min + 2 * y_third, z_min, z_max),
        (x_min + x_third, x_min + 2 * x_third, y_min + y_third, y_min + 2 * y_third, z_min, z_max),
        (x_min + 2 * x_third, x_max, y_min + y_third, y_min + 2 * y_third, z_min, z_max),
        (x_min, x_min + x_third, y_min + 2 * y_third, y_max, z_min, z_max),
        (x_min + x_third, x_min + 2 * x_third, y_min + 2 * y_third, y_max, z_min, z_max),
        (x_min + 2 * x_third, x_max, y_min + 2 * y_third, y_max, z_min, z_max),
    ]

    return subregion_bounds[index]

def filter_vertices(vertices, bounds):
    x_min, x_max, y_min, y_max, z_min, z_max = bounds
    filtered_vertices = []
    vertex_map = {}
    index = 0
    for i, (x, y, z) in enumerate(vertices):
        if x_min <= x <= x_max and y_min <= y <= y_max and z_min <= z <= z_max:
            filtered_vertices.append((x, y, z))
            vertex_map[i] = index
            index += 1
    return filtered_vertices, vertex_map


def filter_faces(faces, vertex_map):
    filtered_faces = []
    for face in faces:
        if all(vertex in vertex_map for vertex in face):
            filtered_faces.append(tuple(vertex_map[vertex] for vertex in face))
    return filtered_faces


def merge_meshes(mesh1, mesh2):
    merged_vertices = mesh1.vertices.tolist() + mesh2.vertices.tolist()
    offset = len(mesh1.vertices)
    merged_faces = mesh1.faces.tolist() + [(f[0] + offset, f[1] + offset, f[2] + offset) for f in mesh2.faces]
    return trimesh.Trimesh(vertices=merged_vertices, faces=merged_faces)


def plot_trimesh(mesh, title):
    mesh.show()


def split_and_load_subregions( vertices, faces, subregion_indices):

    x_bounds, y_bounds, z_bounds = get_bounds(vertices)

    all_filtered_vertices = []
    all_filtered_faces = []
    vertex_offset = 0

    for index in subregion_indices:
        subregion_bounds = get_subregion_bounds(x_bounds, y_bounds, z_bounds, index)
        filtered_vertices, vertex_map = filter_vertices(vertices, subregion_bounds)
        filtered_faces = filter_faces(faces, vertex_map)

        all_filtered_vertices.extend(filtered_vertices)
        all_filtered_faces.extend(
            [(f[0] + vertex_offset, f[1] + vertex_offset, f[2] + vertex_offset) for f in filtered_faces])
        vertex_offset += len(filtered_vertices)

    mesh = trimesh.Trimesh(vertices=all_filtered_vertices, faces=all_filtered_faces)

    # 可视化完整的OBJ文件
    # original_mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    # plot_trimesh(original_mesh, '完整的OBJ文件')

    # 可视化等分后的子区域
    # plot_trimesh(mesh, '子区域')

    return mesh


# 示例用法
# obj_file_path = 'q.obj'
# subregion_indices = [0, 1,2,3]  # 选择前两个子区域
# subregion_mesh = split_and_load_subregions(obj_file_path, subregion_indices)
