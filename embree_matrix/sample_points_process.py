import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


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


def get_bounds(vertices):
    min_x = min(vertices, key=lambda v: v[0])[0]
    max_x = max(vertices, key=lambda v: v[0])[0]
    min_y = min(vertices, key=lambda v: v[1])[1]
    max_y = max(vertices, key=lambda v: v[1])[1]
    min_z = min(vertices, key=lambda v: v[2])[2]
    max_z = max(vertices, key=lambda v: v[2])[2]
    return (min_x, max_x), (min_y, max_y), (min_z, max_z)


def sample_points_in_bounds(x_bounds, y_bounds, z_min, num_points):
    x_min, x_max = x_bounds
    y_min, y_max = y_bounds

    sampled_points = []
    for _ in range(num_points):
        x = random.uniform(x_min, x_max)
        y = random.uniform(y_min, y_max)
        z = z_min  # Set height to the minimum height of the OBJ
        sampled_points.append([x, y, z])

    return sampled_points


def sample_points_from_obj(vertices, faces, num_points):
     # = read_obj_file(obj_file_path)
    x_bounds, y_bounds, z_bounds = get_bounds(vertices)
    z_min = z_bounds[0]
    # print(z_bounds)
    sampled_points = sample_points_in_bounds(x_bounds, y_bounds, z_min, num_points)
    return sampled_points


def plot_points(vertices, sampled_points):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # 提取原始顶点的X、Y、Z坐标
    xs, ys, zs = zip(*vertices)
    ax.scatter(xs, ys, zs, c='b', marker='o', label='OBJ Vertices')

    # 提取采样点的X、Y、Z坐标
    sx, sy, sz = zip(*sampled_points)
    ax.scatter(sx, sy, sz, c='r', marker='^', label='Sampled Points')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('OBJ Vertices and Sampled Points')
    ax.legend()
    plt.show()


# # 示例用法
# obj_file_path = 'q4.obj'
# num_points = 100  # Sample 100 points
# vertices, faces = read_obj_file(obj_file_path)
# sampled_points = sample_points_from_obj(vertices, faces , num_points)
#
# # 读取OBJ文件的顶点以便可视化
#
#
# # 可视化
# plot_points(vertices, sampled_points)
