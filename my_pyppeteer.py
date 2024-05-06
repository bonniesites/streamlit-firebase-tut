import asyncio
from pyppeteer import launch

def build_url(base, tld):
    print('\n\n Building url')
    return f'https://{base}.{tld}'

async def get_screenshot(base, tld):
    print('\n\n Getting screenshot')   
    url = build_url(base, tld)
    browser = await launch()
    page = await browser.newPage()
    await page.goto(url)
    await page.screenshot({'path': f'{url}.png'})
    await browser.close()

async def evaluate_js(base, tld):
    print('\n\n Evaluating JS')  
    url = build_url(base, tld)
    browser = await launch()
    page = await browser.newPage()
    await page.goto(url)
    dimensions = await page.evaluate('''() => {
        return {
            width: document.documentElement.clientWidth,
            height: document.documentElement.clientHeight,
            deviceScaleFactor: window.devicePixelRatio,
        }
    }''')
    print(dimensions)
    await browser.close()

async def main():
    base = 'gotwick'  
    tld = 'com'
    await get_screenshot(base, tld)
    await evaluate_js(base, tld)
    

# To run the main function and handle all asyncio tasks
asyncio.run(main())
print('\n\n')
    