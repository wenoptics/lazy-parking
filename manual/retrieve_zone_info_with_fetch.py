import asyncio
import json
from pprint import pprint
from typing import List, Dict

import pyppeteer
from pyppeteer import launch, network_manager

pyppeteer.DEBUG = True
print("""
This is to get the zone information from the ParkMobile map.

Instructions:
1. Wait for the Chromium to be opened
""")

zone_file = 'zone-data.json'
zone_json = json.load(open(zone_file, 'r+'))  # <zone-id>: { zone-payload }
js_fetch = open('fetch_zones.js').read()


async def process_data(zone_data_payload: [Dict, List]):
    """
    Read queue, append data to JSON

    Data will be keyed by zone-id, so duplicated items will not be kept
    :return:
    """
    print(zone_data_payload)
    if type(zone_data_payload) is not list:
        zone_data_payload = zone_data_payload['zones']
    """
        [
            {
                availability: null
                distanceMiles: 0.0037282260000000003
                internalZoneCode: "2816010"
                locationName: "Pittsburgh, PA"
                parkingActionType: 1
                signageCode: "6010"
                type: "OnStreet"
                typeId: 0
                zoneInfo: {
                    latitude: 40.438729,
                    longitude: -79.987375
                }
                latitude: 40.438729
                longitude: -79.987375
                zoneServices: []
            }
        ]
    """
    print('Get {} from data'.format(len(zone_data_payload)))
    for current in zone_data_payload:
        z_id = current.get('signageCode')

        # Clean up the data:
        current: Dict
        current.pop('distanceMiles')

        zone_json[z_id] = current
    print('Now total data is: ', len(zone_json))
    with open(zone_file, 'w') as file:
        json.dump(zone_json, file, indent=2)


preserved = {
    'headers': {}
}

async def main():

    browser = await launch(devtools=True)
    page = await browser.newPage()
    await page.goto('https://app.parkmobile.io/search')
    await page.waitForSelector('.eyhEak')

    print('[INFO] First page loaded')
    # After we load first page, intercept the next request to get headers
    await page.setRequestInterception(True)

    async def check_request(request: network_manager.Request):
        if not request.url.startswith('https://app.parkmobile.io/api'):
            await request.continue_()
            return
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>')
        print('[DEBUG] API header updated: ', request.url)
        pprint(request.headers)
        print('<<<<<<<<<<<<<<<<<<<<<<<<<<')
        preserved['headers'] = request.headers
        await request.continue_()

    page.on('request', lambda req: asyncio.ensure_future(check_request(req)))
    # And visit the page (again) to intercept headers
    await page.waitFor(2000)
    print('[INFO] Initiate new page for retrieving API request headers')
    await page.goto('https://app.parkmobile.io/search')

    async def fetch_zone(lat1, lon1, lat2, lon2, max_result=100):
        """Use JavaScript to fetch from PM search API. Return a list of zones information"""
        zone_data = await page.evaluate(
            js_fetch,
            lat1, lon1, lat2, lon2,
            max_result,
            json.dumps(preserved['headers']),
            force_expr=False
        )
        return zone_data

    await asyncio.sleep(2)
    z = await fetch_zone(
        40.5140166878681,-79.71802223179839,40.383341065514124,-80.08537757847807,1000
    )
    await process_data(z)

    await browser.close()
    print('All done.')

asyncio.get_event_loop().run_until_complete(main())
