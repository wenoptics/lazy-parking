import math

EARTH_R = 6371  # in Kilometers
P = math.pi / 180
NORTH, EAST, SOUTH, WEST = 0, 90, 180, 270


def lat_lon_2_distance(lat1, lon1, lat2, lon2) -> float:
    """
    Calculation the distance in meters between two (lat, lon) pairs

    :param lat1: latitude value of point A
    :param lon1: longitude value of point A
    :param lat2: latitude value of point B
    :param lon2: longitude value of point B
    :return:
    """
    # Ref: http://powerappsguide.com/blog/post/formulas-calculate-the-distance-between-2-points-longitude-latitude
    a = 0.5 \
        - math.cos((lat2 - lat1) * P) / 2 \
        + math.cos(lat1 * P) * math.cos(lat2 * P) \
        * (1 - math.cos((lon2 - lon1) * P)) / 2

    d = 2 * EARTH_R * math.asin(math.sqrt(a))  # 2*R*asin
    return d * 1000


def lat_lon_bearing_dist(lat, lon, bearing, distance) -> (float, float):
    """
    Given a start point, initial bearing, and distance, returns the destination point
        and final bearing travelling along a (shortest distance) great circle arc.

    :param lat: latitude value of the starting point
    :param lon: longitude value of the starting point
    :param bearing: Bearing direction (clockwise from north)
    :param distance: Distance in meter
    :return:
    """

    """
    REF: https://www.movable-type.co.uk/scripts/latlong.html
    Formula:
        φ2 = asin( sin φ1 ⋅ cos δ + cos φ1 ⋅ sin δ ⋅ cos θ )
        λ2 = λ1 + atan2( sin θ ⋅ sin δ ⋅ cos φ1, cos δ − sin φ1 ⋅ sin φ2 )
        where
            φ is latitude, 
            λ is longitude, 
            θ is the bearing (clockwise from north), 
            δ is the angular distance d/R; 
            d being the distance travelled, 
            R the earth’s radius
    """
    # Distance from meter to KM
    distance = distance / 1000

    # lat, lon to RAD
    lat = lat * P
    lon = lon * P
    bearing = bearing * P

    d_r = distance / EARTH_R
    a = math.sin(lat) * math.cos(d_r)\
        + math.cos(lat) * math.sin(d_r) * math.cos(bearing)
    ret_lat = math.asin(a)

    y = math.sin(bearing) * math.sin(d_r) * math.cos(lat)
    x = math.cos(d_r) - math.sin(lat) * math.sin(ret_lat)
    ret_lon = lon + math.atan2(y, x)

    # Convert from RAD to degree
    ret_lat = ret_lat / P
    ret_lon = ret_lon / P

    # Normalize the longitude to −180, +180
    ret_lon = (ret_lon + 540) % 360 - 180

    return ret_lat, ret_lon
