import json
from read_height import get_height_by_lon_lat
from pyproj import CRS, Transformer

import numpy as np
from scipy.spatial import cKDTree
import pandas as pd
from pyproj import Proj, transform
from tqdm import tqdm
df = pd.read_csv(r"munich_trans_facade_samples.csv")
df['Floor'] = df['Floor'] * 2.4
# 用列的均值替换NaN值
selected_columns = df[['join_xcoor', 'join_ycoor', 'Floor']]
line_list_data=selected_columns.values.tolist()
# 示例 EPSG:25832 点坐标

def convert_epsg25832_to_epsg4326(lon, lat):
    # 创建坐标参考系统
    crs_src = CRS("EPSG:25832")
    crs_dst = CRS("EPSG:4326")

    # 创建转换器
    transformer = Transformer.from_crs(crs_src, crs_dst, always_xy=True)

    # 进行坐标转换
    lon_converted, lat_converted = transformer.transform(lon, lat)
    return lon_converted, lat_converted

def get_points():
    epsg25832_points =   np.array(line_list_data)


    for point in tqdm(epsg25832_points):
        point[2] += get_height_by_lon_lat(convert_epsg25832_to_epsg4326(point[0], point[1]))
        with open('points.jsonl','a') as file:
            file.write(json.dumps({'point':(point.tolist())}))
    np.save('epsg25832_points.npy', epsg25832_points)
    return epsg25832_points

get_points()
