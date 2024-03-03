from ..supermarket_apis import Woolworths, Shoprite
from ..extraction import HeadlessBrowser
from concurrent.futures import ThreadPoolExecutor

def map_function(self, func, container: list):
        with ThreadPoolExecutor() as execute:
            return execute.map(func, container)

if __name__ == '__main__':
    woolies = Woolworths()
    shoprite = Shoprite()
    supermarkets = [woolies]
    HeadlessBrowser.run(supermarkets, 'bacon')