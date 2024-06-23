from datetime import datetime, timedelta

import numpy
import numpy as np
from tqdm import tqdm
import time
# from split_mesh import find_mesh_by_coords
from get_sun_direction import calculate_sunray_direction_vector

import trimesh
def judge_intersection(obj_mesh,origin,direction,date_str):
    intersects = obj_mesh.ray.intersects_any(
        ray_origins=origin,
        ray_directions=direction
    )
    intersects_matrix = intersects.astype(int)  # True转为1, False转为0
    np.save(f'locations_3\locations_{date_str}.npy',intersects_matrix)

# ray_list=[]
def iterate_date(obj_mesh,points_array):
    time_list = {'2024-06-20': ["05:15", "21:45"], '2024-12-21': ["08:30", "16:00"]}

    step_size = 15
    result = []
    for date, times in time_list.items():

        start_dt = datetime.strptime(f"{date} {times[0]}", "%Y-%m-%d %H:%M")
        end_dt = datetime.strptime(f"{date} {times[1]}", "%Y-%m-%d %H:%M")
        num = 0
        with tqdm() as pbar:
            while start_dt <= end_dt:
                # result.append({'date': start_dt.strftime("%Y-%m-%d"), 'time': start_dt.strftime("%H:%M")})
                date_str=start_dt.strftime("%Y-%m-%d")
                time_str=start_dt.strftime("%H:%M")
                sun_vec = calculate_sunray_direction_vector(date_str, time_str)
                expanded_array = np.tile(sun_vec, (len(points_array), len(sun_vec)))
                judge_intersection(obj_mesh,points_array,expanded_array,date_str+"_"+str(time_str).replace(":","__"))

                start_dt += timedelta(minutes=step_size)
                num+=1
                pbar.update(num)




start_time=time.time()
points_array=np.load('closest_point.npy')
obj_mesh=trimesh.load(r"path_to_save_mesh.ply")
# obj_mesh.export('path_to_save_mesh.ply', file_type='ply')
print(time.time()-start_time)
iterate_date(obj_mesh,points_array)
print(time.time()-start_time)
