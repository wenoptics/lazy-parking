import math

EARTH_R = 6371
P = math.pi / 180


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
