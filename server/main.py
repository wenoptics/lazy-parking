import json
from pathlib import Path

from flask import Flask, request, jsonify

from calc_range import RangeFinder

SECRET = '173e7d21-83a0-49aa-88b6-05a62ac7e834'
# SECRET = 'abc'
DATA = Path(__file__).parent / '..' / 'manual' / 'zone-data.json'

obj = json.load(open(DATA))
rf = RangeFinder(obj.values())
app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Auto ParkMobile Home</p>"


@app.route(f"/{SECRET}/park")
def api_park():
    zone_id = request.args.get('zone_id')
    duration_h = float(request.args.get('duration_h', 0))
    duration_m = float(request.args.get('duration_m', 0))
    return jsonify({
        "zone_id": zone_id,
        "duration": duration_h * 60 + duration_m
    })


@app.route(f"/{SECRET}/find_zone")
def api_find_zone():
    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lon'))
    radius = float(request.args.get('radius', 100))
    return jsonify(rf.find_zone_in_range(lat, lon, radius))


if __name__ == "__main__":
    PORT = 5000
    print(f"""
    Try the URLs:
        http://localhost:{PORT}/{SECRET}/find_zone?lat=40.449058&lon=-79.950374&radius=100
        http://localhost:{PORT}/{SECRET}/park?zone_id=1234&duration_h=1&duration_m=20
        
    """)
    app.run(debug=True, port=PORT)
