import numpy as np
import trimesh
from multiprocessing import Pool

def process_rays(chunk):
    return trimesh.load_path(chunk.reshape(-1, 2, 3))

def main():
    # 示例光线的起点和方向
    ray_origins = np.array([[0, 0, 0], [1, 1, 1], [2, 2, 2], [3, 3, 3]])
    ray_directions = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 0]])

    # 计算光线的终点并重塑数组
    ray_endpoints = ray_origins + ray_directions * 200.0
    rays = np.hstack((ray_origins, ray_endpoints)).reshape(-1, 2, 3)

    # 将数据分块
    chunks = np.array_split(rays, 4)  # 分成4块，实际根据CPU核数调整

    # 使用多进程池并行处理
    with Pool(processes=4) as pool:
        results = pool.map(process_rays, chunks)

    # 合并结果
    ray_visualize = trimesh.Scene()
    for result in results:
        ray_visualize.add_geometry(result)

    # 可视化
    ray_visualize.show()

if __name__ == '__main__':
    main()
