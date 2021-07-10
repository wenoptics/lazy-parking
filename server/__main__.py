import asyncio
import atexit
import configparser
from time import sleep

from aiohttp import web
from aiohttp.web import Request, Response

from pm_find_zone import find_zone
from pm import PMLoginVisitor
from pm_parking import api_get_zone_time_block, api_submit_parking
from config import pyppeteer_common

SECRET = '173e7d21-83a0-49aa-88b6-05a62ac7e834'
config = configparser.ConfigParser()
config.read('../.secret')
v = PMLoginVisitor(
    config.get('testauth', 'username'),
    config.get('testauth', 'password'),
    debug=True,
    pyppeteer_kwargs=dict(
        **pyppeteer_common,
        headless=False
    )
)


async def index(request: Request):
    return Response(
        text="<p>Auto ParkMobile Home</p>",
        content_type='text/html'
    )


async def api_park(request: Request):
    zone_id = request.query.get('zoneId')
    billing_method_id = request.query.get('billingMethodId')
    duration_minutes = request.query.get('durationMinutes')
    time_block_id_minutes = request.query.get('timeBlockIdMinutes')
    vehicle_id = request.query.get('vehicleId')

    payload = await api_submit_parking(
        v,
        zone_id=zone_id,
        billing_method_id=billing_method_id,
        duration_minutes=duration_minutes,
        time_block_id_minutes=time_block_id_minutes,
        vehicle_id=vehicle_id,
    )

    return web.json_response({
        "ok": True
    })


async def api_find_zone(request: Request):
    lat = float(request.query.get('lat'))
    lon = float(request.query.get('lon'))
    radius = float(request.query.get('radius') or 100)
    return web.json_response(await find_zone(v, lat, lon, radius))


async def api_get_time_block(request: Request):
    zone_id = request.query.get('zoneId')
    return web.json_response(await api_get_zone_time_block(v, zone_id))


async def setup() -> web.Application:

    @atexit.register
    def clean_up():
        asyncio.ensure_future(v.teardown())
        sleep(2)

    await v.setup_page()
    print('Page setup OK.', v._main_page.url)

    app = web.Application()
    app.router.add_get('/', index)
    app.router.add_get(f'/{SECRET}/park', api_park)
    app.router.add_get(f'/{SECRET}/find_zone', api_find_zone)
    app.router.add_get(f'/{SECRET}/time_block', api_get_time_block)
    return app


if __name__ == "__main__":
    PORT = 5000
    print(f"""
    
    Try the URLs:
        http://localhost:{PORT}/{SECRET}/find_zone?lat=40.449058&lon=-79.950374&radius=100
        http://localhost:{PORT}/{SECRET}/time_block?zoneId=2815560      
        http://localhost:{PORT}/{SECRET}/park?zoneId=2815560&billingMethodId=32551886&durationMinutes=15&timeBlockIdMinutes=125648&vehicleId=41537782        
    """)

    web.run_app(setup(), port=PORT, host='0.0.0.0')
