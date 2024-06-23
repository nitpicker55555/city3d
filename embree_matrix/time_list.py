from datetime import datetime, timedelta

import numpy as np

from get_sun_direction import calculate_sunray_direction_vector
# Dictionary containing dates and time ranges
time_list = {'2024-06-20': ["05:15", "21:45"], '2024-12-21': ["08:30", "16:00"]}

step_size = 15
result=[]
for date, times in time_list.items():

    start_dt = datetime.strptime(f"{date} {times[0]}", "%Y-%m-%d %H:%M")
    end_dt = datetime.strptime(f"{date} {times[1]}", "%Y-%m-%d %H:%M")
    while start_dt <= end_dt:

        date_str = start_dt.strftime("%Y-%m-%d")
        time_str = start_dt.strftime("%H:%M")
        result.append(str(date_str+"_"+time_str))
        # sun_vec = calculate_sunray_direction_vector(date_str, time_str)
        # result.append(sun_vec)
        start_dt += timedelta(minutes=step_size)
  # Display first 10 entries to check correctness
print(result)
# aa=np.array(result)
# print(aa.shape)
# num_points = 1386260
# expanded_matrix = np.tile(aa[:, np.newaxis, :], (1, num_points, 1))
#
# # 检查扩展后的矩阵形状
# print("Shape of the expanded matrix:", expanded_matrix.shape)
# np.save('sun_vec.npy',expanded_matrix)