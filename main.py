import json
import pyperclip

def read_geojson_points(filename):
    points_coordinates = []

    with open(filename, 'r') as file:
        data = json.load(file)

    # 检查GeoJSON是否为FeatureCollection类型
    if data['type'] == 'FeatureCollection':
        for feature in data['features']:
            if feature['geometry']['type'] == 'Point':
                # 提取点的坐标并添加到列表中
                points_coordinates.append(feature['geometry']['coordinates'])

    return points_coordinates


# 使用函数读取本地GeoJSON文件
# 假设文件名为'my_geojson.geojson'
coordinates = read_geojson_points(r"C:\Users\Morning\Desktop\intermediate_points2.geojson")
pyperclip.copy(str(coordinates))
# print(coordinates)
