import time
import numpy as np
import trimesh
from get_sun_direction import calculate_sunray_direction_vector
# load a file by name or from a buffer
# mesh = trimesh.load_mesh(r"q.obj")
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


def cal_intensity(sun_vec, data,model=None):
    # mesh = trimesh.load_mesh(model)
    mesh = model
    def convert(latitude, longitude):
        # print(latitude,longitude)
        return transformer.transform(longitude, latitude)


    # collect_origins = []
    collect_directions = [sun_vec] * len(data)

    # for i in range(len(data)):
    #     # print(data[i])
    #
    #     # collect_origins.append([*convert(data[i][0], data[i][1]), data[i][2]-45])
    #
    #     collect_directions.append(sun_vec)

    ray_origins = np.array(data)
    ray_directions = np.array(collect_directions)
    from embreex import rtcore_scene
    start_time = time.time()
    # run the mesh- ray query
    locations, index_ray, index_tri  = trimesh.ray.ray_pyembree.RayMeshIntersector(mesh).intersects_location(
            ray_origins=ray_origins,
            ray_directions=ray_directions)
    end_time = time.time()
    # stack rays into line segments for visualization as Path3D
    # ray_visualize = trimesh.load_path(np.hstack((ray_origins,
    #                                              ray_origins + ray_directions*500.0)).reshape(-1, 2, 3))
    #

    hit_rays = set(index_ray)
    # print(len(data),'all vec',len(hit_rays),'hit_rays')
    # all_rays = set(range(len(ray_origins)))
    # no_hit_rays = all_rays - hit_rays
    intensity_list=create_custom_list(sorted(list(hit_rays)),len(data))



    # 计算总时间
    total_time = end_time - start_time

    # 输出时间
    # print("time：{:.2f}".format(total_time))
    mesh=''
    return intensity_list,total_time

