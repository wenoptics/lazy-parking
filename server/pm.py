import asyncio
from pprint import pprint

import pyppeteer
from pyppeteer import network_manager
from pyppeteer.page import Page

from visitor import Visitor


class PMVisitor(Visitor):
    URL_API = 'https://app.parkmobile.io/api'


class PMNonLoginVisitor(PMVisitor):
    URL_HOME = 'https://app.parkmobile.io/search'

    async def setup_page(self) -> Page:
        browser = await pyppeteer.launch(devtools=self._debug)
        self._browser = browser
        page = (await browser.pages())[0]
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
        # This is a panel. Upon loaded, indicates the zones are all loaded
        await page.waitForSelector('.eyhEak')

        self._main_page = page
        return page


class PMLoginVisitor(PMVisitor):

    def __init__(self, username, password, debug=False):
        super().__init__(debug=debug)
        self._username = username
        self._password = password

    async def setup_page(self) -> Page:
        browser = await pyppeteer.launch(devtools=self._debug)
        self._browser = browser
        page = (await browser.pages())[0]

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

        login_get_response = await page.goto('https://app.parkmobile.io/login')

        if login_get_response.status == 200:
            # fill login form
            await page.type('input#username', self._username)
            await page.type('input#password', self._password)
            await page.click('button[type="submit"]')
            login_post_response = await page.waitForResponse(
                lambda response: response.url == "https://app.parkmobile.io/api/login")
            if login_post_response.ok:
                print(login_post_response.text)
                print(login_post_response.status)

        self._main_page = page
        return page
