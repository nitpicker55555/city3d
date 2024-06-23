import os
import json
import rasterio
import numpy as np
from pyproj import Transformer
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import multiprocessing
def extract_geolocation_data(tif_file):
    with rasterio.open(tif_file) as dataset:
        # 提取数据和元数据
        data = dataset.read(1)  # 读取第一个波段
        transform = dataset.transform  # 获取仿射变换
        crs = dataset.crs  # 获取坐标参考系统

    # 创建投影转换器，假设 TIF 文件是 EPSG:25832 坐标系
    transformer = Transformer.from_crs(crs, "epsg:4326", always_xy=True)

    # 获取每个像素的行列索引
    rows, cols = np.indices(data.shape)
    rows = rows.flatten()
    cols = cols.flatten()

    # 将行列索引转换为空间坐标
    xs, ys = rasterio.transform.xy(transform, rows, cols)

    # 转换为经纬度坐标
    lons, lats = transformer.transform(xs, ys)

    # 将地面高度和经纬度组合在一起
    heights = data.flatten()
    points = dict()
    for lon, lat, height in zip(lons, lats, heights):
        points[f"{lon:.6f},{lat:.6f}"] = float(height)

    return points

def process_tif_files(folder_path, output_json, max_workers=multiprocessing.cpu_count()):

    tif_files = []

    # 收集所有 TIF 文件路径
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.tif'):
                file_path = os.path.join(root, file)
                tif_files.append(file_path)
    print(max_workers)
    # 使用线程池并行处理 TIF 文件，并使用 tqdm 显示进度条
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(extract_geolocation_data, tif): tif for tif in tif_files}

        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing TIF files"):
            all_points = {}
            tif = futures[future]
            try:
                points = future.result()
                all_points.update(points)
                with open(output_json, 'a') as json_file:
                    json_file.write(json.dumps(all_points)+'\n')
            except Exception as exc:
                print(f"Exception occurred while processing {tif}: {exc}")

    # 保存所有数据到 JSON 文件


    print(f"All data has been saved to {output_json}")

# 设置文件夹路径和输出 JSON 文件路径
folder_path = 'raster'
output_json = 'output_data.json'

process_tif_files(folder_path, output_json, max_workers=8)
