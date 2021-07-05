import asyncio
from pyppeteer import launch, network_manager

async def login(
    username,
    password):

    browser = await launch(headless=False)
    page = await browser.newPage()
    login_get_response = await page.goto('https://app.parkmobile.io/login')

    if login_get_response.status == 200:
        # fill login form
        await page.type('input#username', username)
        await page.type('input#password', password)
        await page.click('button[type="submit"]')
        login_post_response = await page.waitForResponse(lambda response: response.url == "https://app.parkmobile.io/api/login")
        if login_post_response.ok:
            print(login_post_response.text)
            print(login_post_response.status)
    await browser.close()

    #  hours=0, 
    # minutes, 
    # plate, 
    # zone,   
    # # zone
    # await page.type('input#signageCode', zone)
    # await page.click('button[type="submit"]');
    
    # # handle if multiple cities pops up
    # await page.$(".Box__Root-r57gou-0.ddVPGy")
    # pittsburgh = "choose-zone-281" + str(zone)
    # await page.click('button[data-pmtest-id={pittsburgh}]')
    # await page.click('button[data-pmtest-id="confirm-zone"]')

    # # choose time
    # await page.click('input#rate-hour-minutes')
    # await page.select('select#minutes', str(minutes) + " Minutes")
    # await page.select('select#hours', str(hours) + " Hours")
    # await page.click('button[type="submit"]');

    # # choose car
    # if plate == LNJ8640:
    #     plate_selector = 'input#41537782'
    # else:
    #     plate_selector = 'input#22463588'
    # await page.click(plate_selector);
    # await page.click('button[type="submit"]');

    # # continue to pay
    # await page.click('button[type="submit"]');

    
    # # start parking
    # await page.click('button.ButtonBase__Root-mnj4in-0.iZrEhK.Button__Base-sc-15bwt0n-0.Button__PrimaryRoot-sc-15bwt0n-4.csvxiL')
# )

    

asyncio.get_event_loop().run_until_complete(login(
    username="",
    password=""))