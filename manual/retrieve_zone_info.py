import asyncio
import json

import pyppeteer
from pyppeteer import launch, network_manager

pyppeteer.DEBUG = True
print("""
This is to get the zone information from the ParkMobile map.

Instructions:
1. Wait for the Chromium to be opens
2. Browse the map with a smaller zoom level
3. Wait for the parking meter pins to be loaded
4. Go to 2 and repeat till the desired areas are all covered
""")

zone_file = 'zone-data.json'
a_queue = asyncio.queues.Queue()
zone_json = json.load(open(zone_file, 'r+'))  # <zone-id>: { zone-payload }


async def add_payload(r: network_manager.Response):
    data = await r.json()
    print('===\n', r.url)
    print(data)
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
    zooms = data.get('zones', [])
    print('Get {} from data'.format(len(zooms)))
    await asyncio.gather(*[a_queue.put(zone) for zone in zooms])


async def sort_data():
    """
    Read queue, append data to JSON

    Data will be keyed by zone-id, so duplicated items will not be kept
    :return:
    """
    try:
        while True:
            current = a_queue.get_nowait()
            z_id = current.get('signageCode')
            zone_json[z_id] = current
    except asyncio.queues.QueueEmpty:
        pass
    print('Now total data is: ', len(zone_json))
    with open(zone_file, 'w') as file:
        json.dump(zone_json, file, indent=2)


async def main():

    def on_response(r: network_manager.Response):
        """Submit a async task from a sync func (Since .on only accept sync callback)"""
        if not r.url.startswith('https://app.parkmobile.io/api/zones/search'):
            return
        asyncio.create_task(add_payload(r))

    browser = await launch(devtools=True)
    page = await browser.newPage()
    page.on('response', on_response)
    await page.goto('https://app.parkmobile.io/search')
    # await page.screenshot({'path': 'example.png'})
    # await browser.close()
    while True:
        await asyncio.sleep(2)
        await sort_data()

asyncio.get_event_loop().run_until_complete(main())
