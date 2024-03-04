from .headless_browser import headless_browser
from concurrent.futures import ThreadPoolExecutor
from supermarket_apis import Woolworths, Shoprite, PicknPay

def map_function(self, func, container: list):
    with ThreadPoolExecutor() as execute:
        return execute.map(func, container)

if __name__ == '__main__':
    woolies = Woolworths()
    #shoprite = Shoprite()
    #pnp = PicknPay()
    headless_browser(woolies, 'muffins')