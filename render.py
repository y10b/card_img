"""posts/*/slides.html 의 각 <section class="slide"> 를 1080x1350 JPG로 렌더링한다."""
import asyncio, glob, os
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 1080, 'height': 1350})
        for html in sorted(glob.glob('posts/*/slides.html')):
            d = os.path.dirname(html)
            await pg.goto('file://' + os.path.abspath(html))
            await pg.evaluate('document.fonts.ready')
            await pg.wait_for_timeout(1500)
            slides = await pg.query_selector_all('section.slide')
            for i, el in enumerate(slides, 1):
                await el.screenshot(path=f'{d}/card_{i:02d}.jpg', type='jpeg', quality=88)
            print(d, len(slides), 'cards')
        await b.close()

asyncio.run(main())
