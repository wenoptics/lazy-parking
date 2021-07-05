import asyncio

from utils import lat_lon_bearing_dist, NORTH, WEST, EAST, SOUTH
from visitor import Visitor


def find_zone(v: Visitor, lat, lon, square_radius=100):
    """
    Find all parking zones within a square radius of a given lat-lon coordination
    :param v:
    :param lat:
    :param lon:
    :param square_radius: in meters
    :return:
    """

    lat_top, _ = lat_lon_bearing_dist(lat, lon, NORTH, square_radius)
    lat_bottom, _ = lat_lon_bearing_dist(lat, lon, SOUTH, square_radius)
    _, lon_left = lat_lon_bearing_dist(lat, lon, WEST, square_radius)
    _, lon_right = lat_lon_bearing_dist(lat, lon, EAST, square_radius)

    upper = max(lat_top, lat_bottom), max(lon_left, lon_right)
    lower = min(lat_top, lat_bottom), min(lon_left, lon_right)

    return api_search_zone(v, *(upper), *(lower))


async def api_search_zone(
        v: Visitor,
        upper_lat, upper_lon, lower_lat, lower_lon
):
    url = 'https://app.parkmobile.io/api/zones/search'
    parking_type = '1'

    url = f'{url}?parkingType={parking_type}'
    url += f'&upper={upper_lat},{upper_lon}'
    url += f'&lower={lower_lat},{lower_lon}'

    print('[DEBUG] api_search_zone:', url)
    zone_data = await v.js_fetch('GET', url)
    return zone_data


if __name__ == '__main__':
    from server.pm import PMNonLoginVisitor

    async def simple_run():
        v = PMNonLoginVisitor(debug=True)
        try:
            await v.setup_page()

            zones = await api_search_zone(v, 40.5140166878681, -79.71802223179839, 40.383341065514124, -80.08537757847807)
            # from pprint import pprint; pprint(zones)
            print(len(zones.get('zones')))
            print(zones)

            print('======')

            zones = await find_zone(v, 40.449058, -79.950374, 100)
            # from pprint import pprint; pprint(zones)
            print(len(zones.get('zones')))
            print(zones)

        finally:
            await v.teardown()


    asyncio.run(simple_run())
