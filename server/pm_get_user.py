import asyncio

from config import pyppeteer_common
from visitor import Visitor


async def api_get_user(
        v: Visitor
):
    url = 'https://app.parkmobile.io/api/user'

    print('[DEBUG] api_get_user:', url)
    user_data = await v.js_fetch('GET', url)
    return user_data


if __name__ == '__main__':
    from pm import PMLoginVisitor
    import configparser

    config = configparser.ConfigParser()
    config.read('../.secret')

    async def simple_run():
        v = PMLoginVisitor(
            config.get('testauth', 'username'),
            config.get('testauth', 'password'),
            debug=True,
            pyppeteer_kwargs={
                **pyppeteer_common,
                'devtools': True
            }
        )
        try:
            await v.setup_page()

            zones = await api_get_user(v)
            from pprint import pprint; pprint(zones)

        finally:
            await v.teardown()


    asyncio.run(simple_run())
