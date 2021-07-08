import asyncio
from typing import List

from pyppeteer.errors import ElementHandleError

from visitor import Visitor


async def api_get_zone_time_block(v: Visitor, zone_id):
    """
    Returns time block options in minutes
    :param v:
    :param zone_id:
    :return: Tuple of (time_block_id, [minutes_options])
    """
    zone_id = str(zone_id)

    url = f'https://app.parkmobile.io/api/proxy/parkmobileapi/zone/{zone_id}?'
    print('[DEBUG] api_get_zone_time_block:', url)

    data = await v.js_fetch('GET', url)
    zone = next(filter(lambda i: i.get('internalZoneCode') == zone_id, data['zones']))

    time_blocks = zone['parkInfo']['timeBlocks']
    tb_in_min = next(filter(lambda i: i.get('timeBlockUnit') == 'Minutes', time_blocks))

    time_block_id = tb_in_min['timeblockId']

    allow_min = tb_in_min['minimumValue']
    allow_max = tb_in_min['maximumValue']
    allow_interval = tb_in_min['incrementValue']
    minute_options: List[int] = list(range(allow_min, allow_max, allow_interval)) + [allow_max]

    return time_block_id, minute_options


async def api_get_parking_price(
        v: Visitor
):
    url = 'https://app.parkmobile.io/api/proxy/parkmobileapi/parking/price/2815543?selectedBillingMethodId=32551886&timeBlockId=125648&timeBlockQuantity=45&vehicleId=22463588'

    print('[DEBUG] api_get_parking_price:', url)
    data = await v.js_fetch('GET', url)
    return data


async def api_submit_parking(
        v: Visitor,
        billing_method_id,
        duration_minutes,
        time_block_id_minutes,
        vehicle_id,
        zone_id
):
    url = 'https://app.parkmobile.io/api/proxy/parkmobileapi/parking/active'

    print('[DEBUG] api_get_user:', url)
    parking_info = await v.js_fetch(
        'POST', url,
        headers={
            "content-type": "application/json;charset=UTF-8"
        },
        body={
            "durationInMinutes": int(duration_minutes),
            "internalZoneCode": str(zone_id),
            "selectedBillingMethodId": str(billing_method_id),
            "timeBlockId": int(time_block_id_minutes),
            "vehicleId": str(vehicle_id)
        }
    )
    return parking_info


if __name__ == '__main__':
    from server.pm import PMLoginVisitor
    from pprint import pprint
    import configparser

    config = configparser.ConfigParser()
    config.read('../.secret')

    async def simple_run():
        v = PMLoginVisitor(
            config.get('testauth', 'username'),
            config.get('testauth', 'password'),
            debug=True)
        try:
            await v.setup_page()

            print('=' * 10)
            data = await api_get_parking_price(v)
            pprint(data)
            print('=' * 10)

            print('=' * 10)
            zones = await api_submit_parking(
                v,
                billing_method_id=32551886,
                duration_minutes=15,
                time_block_id_minutes=125648,
                vehicle_id=41537782,
                zone_id=2815560
            )
            pprint(zones)
            print('=' * 10)

            await asyncio.sleep(10000)

        finally:
            await v.teardown()


    asyncio.run(simple_run())
