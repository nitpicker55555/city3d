import time
import numpy as np
import trimesh
from get_sun_direction import calculate_sunray_direction_vector
# load a file by name or from a buffer
mesh = trimesh.load_mesh(r"Munich_center_9_tiles.obj")
from pyproj import Transformer
transformer = Transformer.from_crs("EPSG:4326", "EPSG:25832")




def create_custom_list(index_list, length):
    # 创建一个全为1的列表
    output_list = [1] * length

    # 将index_list中的位置设置为0
    for index in index_list:
        if 0 <= index < length:
            output_list[index] = 0

    return output_list


def cal_intensity(sun_vec, data):


    start_time = time.time()



    def convert(latitude, longitude):
        # print(latitude,longitude)
        return transformer.transform(longitude, latitude)


    collect_origins = []
    collect_directions = []

    for i in range(len(data)):
        # print(data[i])

        collect_origins.append([*convert(data[i][0], data[i][1]), data[i][2]-45])

        collect_directions.append(sun_vec)

    ray_origins = np.array(collect_origins)
    ray_directions = np.array(collect_directions)
    from embreex import rtcore_scene
    # run the mesh- ray query
    locations, index_ray, index_tri  = trimesh.ray.ray_pyembree.RayMeshIntersector(mesh).intersects_location(
            ray_origins=ray_origins,
            ray_directions=ray_directions)
    # stack rays into line segments for visualization as Path3D
    # ray_visualize = trimesh.load_path(np.hstack((ray_origins,
    #                                              ray_origins + ray_directions*500.0)).reshape(-1, 2, 3))
    #
    print(len(collect_origins))
    hit_rays = set(index_ray)
    print(len(hit_rays),'hit_rays')
    # all_rays = set(range(len(ray_origins)))
    # no_hit_rays = all_rays - hit_rays
    intensity_list=create_custom_list(sorted(list(hit_rays)),len(collect_origins))

    end_time = time.time()

    # 计算总时间
    total_time = end_time - start_time

    # 输出时间
    print("总计算时间：{:.2f} 秒".format(total_time))

    return intensity_list

