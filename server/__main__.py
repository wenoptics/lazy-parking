from aiohttp import web
from aiohttp.web import Request, Response

from pm_find_zone import find_zone
from pm import PMNonLoginVisitor

SECRET = '173e7d21-83a0-49aa-88b6-05a62ac7e834'
v = PMNonLoginVisitor(debug=True)


async def index(request: Request):
    return Response(
        text="<p>Auto ParkMobile Home</p>",
        content_type='text/html'
    )


async def api_park(request: Request):
    zone_id = request.query.get('zone_id')
    duration_h = float(request.query.get('duration_h') or 0)
    duration_m = float(request.query.get('duration_m') or 0)
    return web.json_response({
        "zone_id": zone_id,
        "duration": duration_h * 60 + duration_m
    })


async def api_find_zone(request: Request):
    lat = float(request.query.get('lat'))
    lon = float(request.query.get('lon'))
    radius = float(request.query.get('radius') or 100)
    return web.json_response(find_zone(v, lat, lon, radius))


async def setup() -> web.Application:
    await v.setup_page()
    print('Page setup OK.', v._main_page.url)

    app = web.Application()
    app.router.add_get('/', index)
    app.router.add_get(f'/{SECRET}/park', api_park)
    app.router.add_get(f'/{SECRET}/find_zone', api_find_zone)
    return app


if __name__ == "__main__":
    PORT = 5000
    print(f"""
    
    Try the URLs:
        http://localhost:{PORT}/{SECRET}/find_zone?lat=40.449058&lon=-79.950374&radius=100
        http://localhost:{PORT}/{SECRET}/park?zone_id=1234&duration_h=1&duration_m=20
        
    """)

    web.run_app(setup(), port=PORT)
