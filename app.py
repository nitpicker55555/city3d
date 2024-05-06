from flask import Flask, jsonify, request
import json
app = Flask(__name__)
def read_geojson_points(geo_json):
    points_coordinates = []
    data = geo_json
    if data['type'] == 'FeatureCollection':
        for feature in data['features']:
            if feature['geometry']['type'] == 'Point':
                points_coordinates.append(feature['geometry']['coordinates'])

    return points_coordinates
@app.route('/get-list', methods=['GET'])
def get_list():
    # 这里是你想要传递给前端的列表
    data = read_geojson_points()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
