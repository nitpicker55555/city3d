import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

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

def point_in_triangle(p, v0, v1, v2):
    # Using barycentric coordinates to check if point p is inside triangle v0v1v2
    d00 = np.dot(v0 - v2, v0 - v2)
    d01 = np.dot(v0 - v2, v1 - v2)
    d11 = np.dot(v1 - v2, v1 - v2)
    d20 = np.dot(p - v2, v0 - v2)
    d21 = np.dot(p - v2, v1 - v2)
    denom = d00 * d11 - d01 * d01
    v = (d11 * d20 - d01 * d21) / denom
    w = (d00 * d21 - d01 * d20) / denom
    u = 1.0 - v - w
    return (u >= 0) and (v >= 0) and (w >= 0)

def ray_intersects_triangle(p, d, v0, v1, v2):
    epsilon = 1e-8
    e1 = v1 - v0
    e2 = v2 - v0
    h = np.cross(d, e2)
    a = np.dot(e1, h)
    if -epsilon < a < epsilon:
        return False
    f = 1.0 / a
    s = p - v0
    u = f * np.dot(s, h)
    if u < 0.0 or u > 1.0:
        return False
    q = np.cross(s, e1)
    v = f * np.dot(d, q)
    if v < 0.0 or u + v > 1.0:
        return False
    t = f * np.dot(e2, q)
    return t > epsilon

def point_in_mesh(point, vertices, faces):
    # Use ray-casting algorithm to determine if point is inside mesh
    ray_direction = np.array([1.0, 0.0, 0.0])  # Arbitrary direction
    intersections = 0
    for face in faces:
        v0, v1, v2 = vertices[face[0]], vertices[face[1]], vertices[face[2]]
        v0, v1, v2 = np.array(v0), np.array(v1), np.array(v2)
        if ray_intersects_triangle(point, ray_direction, v0, v1, v2):
            intersections += 1
    return intersections % 2 == 1

def sample_points_in_mesh(vertices, faces, num_points):
    x_bounds, y_bounds, z_bounds = get_bounds(vertices)
    x_min, x_max = x_bounds
    y_min, y_max = y_bounds
    z_min, z_max = z_bounds

    sampled_points = []
    while len(sampled_points) < num_points:
        x = random.uniform(x_min, x_max)
        y = random.uniform(y_min, y_max)
        z = random.uniform(z_min, z_max)
        point = np.array([x, y, z])
        if point_in_mesh(point, vertices, faces):
            sampled_points.append(point)

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

# Example usage:
obj_file_path = 'q.obj'
vertices, faces = read_obj_file(obj_file_path)
sampled_points = sample_points_in_mesh(vertices, faces, 100)
plot_points(vertices, sampled_points)
