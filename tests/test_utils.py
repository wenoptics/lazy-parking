from server.utils import lat_lon_2_distance


def test_dist_calc():
    lat1, lon1 = 40.42789, -79.969596
    lat2, lon2 = 40.428606, -79.967927
    d = lat_lon_2_distance(lat1, lon1, lat2, lon2)
    assert d
