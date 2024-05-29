import numpy as np
import pandas as pd
from pvlib.solarposition import get_solarposition
import pytz
def calculate_sunray_direction_vector(date_str, time_str, latitude=48.1443432, longitude=11.5745611, elevation=500):
    """
    计算给定日期、时间和地点的太阳射线三维方向向量。

    参数:
    latitude (float): 纬度
    longitude (float): 经度
    date_str (str): 日期，格式为 'YYYY-MM-DD'
    time_str (str): 时间，格式为 'HH:MM'
    elevation (float): 海拔高度，单位为米

    返回:
    numpy.array: 包含 [x, y, z] 方向向量的数组
    """
    # 创建时间戳
    datetime_str = f"{date_str} {time_str}"
    local_tz = pytz.timezone('Europe/Berlin')  # 德国时区
    local_time = local_tz.localize(pd.to_datetime(datetime_str))
    utc_time = local_time.astimezone(pytz.utc)

    # 转换为 UTC 时间的 DatetimeIndex
    datetime_index = pd.DatetimeIndex([utc_time], tz='UTC')
    # 获取太阳位置
    solar_position = get_solarposition(datetime_index, latitude, longitude)
    azimuth = np.radians(solar_position['azimuth'].iloc[0])
    elevation_angle = np.radians(solar_position['elevation'].iloc[0])

    # 计算方向向量
    x = np.cos(elevation_angle) * np.sin(azimuth)
    y = np.cos(elevation_angle) * np.cos(azimuth)
    z = np.sin(elevation_angle)
    # print(np.array([x, y, z]),'sun_vec',date_str,time_str,latitude,longitude)
    return np.array([x, y, z])

# 测试函数
# date_str = '2024-05-14'
# time_str = '12:00'
# latitude = 48.1443432  # 例如：慕尼黑
# longitude = 11.5745611
#
# direction_vector = calculate_sunray_direction_vector(date_str, time_str, latitude, longitude)
# print(f"太阳射线方向向量: {direction_vector}")
