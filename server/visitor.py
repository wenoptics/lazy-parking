from typing import Dict, Optional, Any

from pyppeteer import launch
from pyppeteer.browser import Browser
from pyppeteer.page import Page


class Visitor:

    def __init__(self, debug=False):
        self._preserved_headers: Dict = {}
        self._debug: bool = debug
        self._main_page: Page = None
        self._browser: Browser = None

    async def setup_page(self) -> Page:
        browser = await launch(devtools=self._debug)
        self._browser = browser
        page = await browser.newPage()
        self._main_page = page
        return page

    async def teardown(self):
        await self._browser.close()

    async def js_fetch(
            self,
            method='GET',
            url: str = '',
            headers: Optional[Dict] = None,
            body: [Dict, str, None] = None
    ) -> Any:
        js_function = """
        (method, url, headers, body) => {
          const parsedHeaders = typeof headers === 'string' ? JSON.parse(headers) : headers

          const req = fetch(url, {
            method,
            mode: 'cors', // no-cors, *cors, same-origin
            credentials: 'same-origin', // include, *same-origin, omit
            headers: parsedHeaders,
            redirect: 'follow', // manual, *follow, error
            referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
            body // body data type must match "Content-Type" header
          })

          console.log('New JS fetch: ', url, parsedHeaders, body, req)
          return req.then(resp => resp.json())
        }
        """
        if headers is None:
            headers = {}
        args = [
            method,
            url,
            {**self._preserved_headers, **headers}
        ]
        if body:
            args.append(body)
        return await self._main_page.evaluate(
            js_function, *args, force_expr=False
        )

    async def fetch(
            self,
            method='GET',
            url: str = '',
            headers: Optional[Dict] = None,
            body: [Dict, str, None] = None
    ) -> Any:
        pass
