import numpy as np


def calculate_light_intensity(occlusion_matrix, normal_matrix, sunlight_matrix):
    """
    计算每个点在每个光线下的光线强度，考虑遮挡和太阳光线与法向量的夹角。

    参数:
    occlusion_matrix (numpy.ndarray): 遮挡矩阵，形状为 (num_rays, num_points)，1 表示遮挡，0 表示未遮挡。
    normal_matrix (numpy.ndarray): 法向量矩阵，形状为 (num_points, 3)，表示每个点的法向量。
    sunlight_matrix (numpy.ndarray): 太阳光线矩阵，形状为 (num_rays, num_points, 3)，表示每个点的太阳光线。

    返回:
    numpy.ndarray: 光线强度矩阵，形状为 (num_rays, num_points)。
    """
    num_rays = occlusion_matrix.shape[0]
    num_points = normal_matrix.shape[0]

    # 确保法向量是单位向量
    normal_matrix /= np.linalg.norm(normal_matrix, axis=1)[:, np.newaxis]

    # 扩展法向量矩阵以匹配太阳光线矩阵的形状
    expanded_normal_matrix = np.repeat(normal_matrix[np.newaxis, :, :], num_rays, axis=0)

    # 计算太阳光线和法向量的点乘
    dot_product = np.sum(expanded_normal_matrix * sunlight_matrix, axis=2)

    # 将点乘结果中的负数置为0
    dot_product = np.maximum(dot_product, 0)

    # 应用遮挡矩阵，计算最终的光线强度矩阵
    intensity_matrix = dot_product * occlusion_matrix

    return intensity_matrix


# 示例数据生成（需要真实数据替换这些）
# num_rays = 98
# num_points = 1386260
occlusion_matrix = np.load('intersection_sum.npy')
normal_matrix = np.load('saved_normals.npy')
sunlight_matrix = np.load('sun_vec.npy')

# 调用函数计算光线强度
intensity_matrix = calculate_light_intensity(occlusion_matrix, normal_matrix, sunlight_matrix)
np.save("intensity.npy",intensity_matrix)
print(intensity_matrix.shape)
# 打印一部分结果以进行检查
print(intensity_matrix[:5, :100])  # 输出前5个光线条件下前10个点的光线强度
