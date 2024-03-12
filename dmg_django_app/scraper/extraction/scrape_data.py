from .headless_browser import Scraper
from concurrent.futures import ThreadPoolExecutor
from ..supermarket_apis import Woolworths, Shoprite, Makro, PicknPay, Checkers

def map_function(self, func, container: list):
    with ThreadPoolExecutor() as execute:
        return execute.map(func, container)

if __name__ == '__main__':
    woolies = Woolworths()
    shoprite = Shoprite()
    pnp = PicknPay()
    checkers = Checkers()
    makro = Makro()
    scraper = Scraper([pnp])
    scraper.scrape_all_data()