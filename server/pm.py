import asyncio
from pprint import pprint
from typing import Dict

import pyppeteer
from pyppeteer import network_manager
from pyppeteer.page import Page

from visitor import Visitor


class PMVisitor(Visitor):
    URL_API = 'https://app.parkmobile.io/api'

    def _update_headers(self, new_headers: Dict):
        for h in new_headers:
            if h not in self._preserved_headers:
                print('[DEBUG] New header "{}" added: "{}"'
                      .format(h, new_headers[h]))
                self._preserved_headers[h] = new_headers[h]
            if self._preserved_headers.get(h) != new_headers[h]:
                print('[DEBUG] header "{}" updated from "{}" to "{}"'
                      .format(h, self._preserved_headers[h], new_headers[h]))
                self._preserved_headers[h] = new_headers[h]

    async def _setup_api_request_interception(self, page: Page):
        await page.setRequestInterception(True)

        async def check_request(request: network_manager.Request):
            if not request.url.startswith(self.URL_API):
                await request.continue_()
                return
            if self._debug:
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>')
                print('[DEBUG] Checking API header from: ', request.url)
            self._update_headers(request.headers)
            if self._debug:
                print('<<<<<<<<<<<<<<<<<<<<<<<<<<')
            await request.continue_()

        page.on('request', lambda req: asyncio.ensure_future(check_request(req)))


class PMNonLoginVisitor(PMVisitor):
    # Just need any page that will initiate any /api request
    URL_HOME = 'https://app.parkmobile.io/zone/7143641'

    async def setup_page(self) -> Page:
        browser = await pyppeteer.launch(**self._pyppeteer_kwargs)
        self._browser = browser
        page = (await browser.pages())[0]
        self._main_page = page
        await self._setup_api_request_interception(page)

        # And visit the page (again) to intercept headers
        await page.waitFor(500)
        print('[INFO] Initiate page for retrieving API request headers')
        await page.goto(self.URL_HOME)

        # Just wait for any /api request to finished
        await page.waitForResponse(
            lambda response: response.url.startswith(self.URL_API))

        await page.waitFor(500)

        return page


class PMLoginVisitor(PMVisitor):

    def __init__(self, username, password, debug=False, pyppeteer_kwargs=None):
        super().__init__(debug=debug, pyppeteer_kwargs=pyppeteer_kwargs)
        self._username = username
        self._password = password

    async def setup_page(self) -> Page:
        browser = await pyppeteer.launch(**self._pyppeteer_kwargs)
        self._browser = browser
        page = (await browser.pages())[0]
        self._main_page = page

        await self._setup_api_request_interception(page)

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

        return page


class PMLoginNewVisitor(PMNonLoginVisitor):

    def __init__(self, username, password, debug=False, pyppeteer_kwargs=None):
        super().__init__(debug=debug, pyppeteer_kwargs=pyppeteer_kwargs)
        self._username = username
        self._password = password

    async def setup_page(self) -> Page:
        page = await super(PMLoginNewVisitor, self).setup_page()

        await page.waitFor(500)
        await page.goto('https://app.parkmobile.io/login')

        login_ok = await super().js_fetch('POST', 'https://app.parkmobile.io/api/login', headers={
            "sec-ch-ua": '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
            "sec-ch-ua-mobile": "?1",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors"
        }, body={
            'email': self._username,
            'password': self._password
        }, return_json=False) == 'OK'

        if not login_ok:
            raise Exception('Login failed')

        return page
