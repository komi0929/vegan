import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.set_viewport_size({'width': 1280, 'height': 4000})
        await page.goto('http://localhost:62022/en/index.html')
        await page.screenshot(path='screenshot_en.png', full_page=True)
        await browser.close()

asyncio.run(main())
