from discount_my_groceries.dmg_django.dmg_django_app.scraper.supermarket_apis.base_api import Supermarket
#from playwright.async_api import async_playwright, Route
from supermarket_apis.woolworths_api import Woolworths
import asyncio

async def handle_route(route: Route) -> None:
    """Modifies the response header,
    'content-type': 'text/html'."""
    
    response = await route.fetch()
    body = await response.text()
    body = await body.replace("<title>", "<title>Modified Response")
    await route.fulfill(
        response=response,
        body=body,
        headers={**response.headers, "content-type": "text/html"},
    )

async def browse_and_scrape(sm: Supermarket) -> None:
    """Captures the product data from a supermarket website."""
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(
            #proxy={
            #    "server": "http://pr.oxylabs.io:7777",
            #    "username": "USERNAME",
            #    "password": "PASSWORD"
            #  },
            headless=False
        )

        context = await browser.new_context()
        page = await context.new_page()

        # Abort image loading
        #await context.route("**/*.{png,jpg,jpeg,svg}", lambda route: route.abort())
        #await context.route("**/*", handle_route)
        
        response = await page.goto(sm.products_page_url(page_number=480), timeout=120000)
        assert response.status != 404

        # Get page selectors.
        list_selector = sm.get_page_selectors()['product_list']
        id_selector = sm.get_page_selectors()['product_id']
        title_selector = sm.get_page_selectors()['product_title']
        alt_title_selector = ''
        if 'alt_product_title' in (sm.get_page_selectors()).keys():
            alt_title_selector = sm.get_page_selectors()['alt_product_title']
        price_selector = sm.get_page_selectors()['product_price']
        promotion_selector = sm.get_page_selectors()['product_promo']
        image_selector = sm.get_page_selectors()['product_img']

        # Store the list of the products.
        product_list = await page.query_selector_all(list_selector)

        # a flag to signal page scrolling.
        scrolldown = 1

        # page scrolling intervals.
        scrolling_intervals = range(4, 61, 4)

        for product in product_list:
            id = await product.query_selector(id_selector)
            if id != None:
                print(str(await id.get_attribute('id')).split('_')[-1])
            
            title = await product.query_selector(title_selector)
            if title != None:
                print(await title.inner_text())
            else:
                title = await product.query_selector(alt_title_selector)
                print(await title.inner_text())

            price = await product.query_selector(price_selector)
            if price != None:    
                print(await price.inner_text())

            promotion = await product.query_selector(promotion_selector)
            if promotion != None:
                print(await promotion.inner_text())

            image = await product.query_selector(image_selector)
            if image != None:
                print(await image.get_attribute('src'))

            print("\n")
            
            if scrolldown in scrolling_intervals:
                await page.keyboard.down('PageDown')

            scrolldown += 1 

        await context.close()    
        await browser.close()

if __name__ == "__main__":
    woolworths = Woolworths()
    asyncio.run(browse_and_scrape(woolworths))
