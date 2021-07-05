import asyncio

from visitor import Visitor


def find_zone(v: Visitor, lat, lon, square_radius):
    return []


async def api_search_zone(
        v: Visitor,
        upper_lat, upper_lon, lower_lat, lower_lon
):
    url = 'https://app.parkmobile.io/api/zones/search'
    parking_type = '1'

    url = f'{url}?parkingType={parking_type}'
    url += f'&upper={upper_lat},{upper_lon}'
    url += f'&lower={lower_lat},{lower_lon}'

    zone_data = await v.js_fetch('GET', url)
    return zone_data


if __name__ == '__main__':
    from server.pm import PMNonLoginVisitor

    async def simple_run():
        v = PMNonLoginVisitor(debug=True)
        await v.setup_page()
        zones = await api_search_zone(v, 40.5140166878681, -79.71802223179839, 40.383341065514124, -80.08537757847807)
        await v.teardown()

        # from pprint import pprint; pprint(zones)
        print(len(zones.get('zones')))
        print(zones)

    asyncio.run(simple_run())
