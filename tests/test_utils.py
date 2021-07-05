from server.utils import lat_lon_2_distance, lat_lon_bearing_dist


def test_dist_calc():
    lat1, lon1 = 40.42789, -79.969596
    lat2, lon2 = 40.428606, -79.967927
    d = lat_lon_2_distance(lat1, lon1, lat2, lon2)
    assert d


def test_bearing_calc():
    lat_start, lon_start = 40.42789, -79.969596
    distance = 100

    for b in (0, 90, 180, 270):
        lat, lon = lat_lon_bearing_dist(
            lat_start,
            lon_start,
            b,
            distance
        )

        d2 = lat_lon_2_distance(
            lat_start, lon_start, lat, lon
        )
        assert d2 - distance < 1  # Calculation error should less than 1 meter
