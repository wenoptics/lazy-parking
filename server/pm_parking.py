import asyncio

from pyppeteer.errors import ElementHandleError

from visitor import Visitor


async def api_get_promo(
        v: Visitor
):
    url = 'https://app.parkmobile.io/api/proxy/parkmobileapi/account/promos'

    print('[DEBUG] api_get_promo:', url)
    try:
        data = await v.js_fetch('POST', url, body={
            'promoCode': "fwenvd"
        })
    except ElementHandleError as e:
        print('[ERROR]', str(e))
        return
    return data


async def api_get_parking_price(
        v: Visitor
):
    url = 'https://app.parkmobile.io/api/proxy/parkmobileapi/parking/price/2815543?selectedBillingMethodId=32551886&timeBlockId=125648&timeBlockQuantity=45&vehicleId=22463588'

    print('[DEBUG] api_get_parking_price:', url)
    data = await v.js_fetch('GET', url)
    return data


async def api_submit_parking(
        v: Visitor
):
    url = 'https://app.parkmobile.io/api/proxy/parkmobileapi/parking/active'

    print('[DEBUG] api_get_user:', url)
    parking_info = await v.js_fetch(
        'POST', url,
        headers={
            "content-type": "application/json;charset=UTF-8"
        },
        body={
            "durationInMinutes": 15,
            "internalZoneCode": "2815543",
            "selectedBillingMethodId": "32551886",
            "timeBlockId": 125648,
            "vehicleId": "22463588"
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
            zones = await api_submit_parking(v)
            pprint(zones)
            print('=' * 10)

            await asyncio.sleep(10000)

        finally:
            await v.teardown()


    asyncio.run(simple_run())
