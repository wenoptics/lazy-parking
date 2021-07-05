import asyncio
from pprint import pprint

import pyppeteer
from pyppeteer import network_manager
from pyppeteer.page import Page

from visitor import Visitor


class PMNonLoginVisitor(Visitor):
    URL_HOME = 'https://app.parkmobile.io/search'
    URL_API = 'https://app.parkmobile.io/api'

    async def setup_page(self) -> Page:
        browser = await pyppeteer.launch(devtools=self._debug)
        self._browser = browser
        page = await browser.newPage()
        await page.setRequestInterception(True)

        async def check_request(request: network_manager.Request):
            if not request.url.startswith(self.URL_API):
                await request.continue_()
                return
            if self._debug:
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>')
                print('[DEBUG] API header updated: ', request.url)
                pprint(request.headers)
                print('<<<<<<<<<<<<<<<<<<<<<<<<<<')
            self._preserved_headers = request.headers
            await request.continue_()

        page.on('request', lambda req: asyncio.ensure_future(check_request(req)))
        # And visit the page (again) to intercept headers
        await page.waitFor(1000)
        print('[INFO] Initiate page for retrieving API request headers')
        await page.goto(self.URL_HOME)
        await page.waitForSelector('.eyhEak')

        self._main_page = page
        return page
