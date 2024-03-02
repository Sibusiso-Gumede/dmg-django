from supermarket_apis import Woolworths, Shoprite
from extraction import HeadlessBrowser
from transformation import retrieve_webpage

if __name__ == '__main__':
    #woolies = Woolworths()
    shoprite = Shoprite()
    supermarkets = [shoprite]
    HeadlessBrowser.run_headless_browser(supermarkets, 'bread')