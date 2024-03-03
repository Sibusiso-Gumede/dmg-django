from ..supermarket_apis import Supermarket
from bs4 import BeautifulSoup
import requests

class StaticSpider():
    def run(supermarket: Supermarket, product_name: str):

        response: requests.Response
        if supermarket.query_parameters:
            response = requests.get(supermarket.get_home_page_url(), params=supermarket.parameters)
        else:
            response = requests.get(supermarket.get_home_page_url()+product_name)

        page = BeautifulSoup(response.content, 'lxml')    
        products = page.select(supermarket.get_page_selectors()['product_list'])
        
        for product in products:
            product_title = product.select_one(supermarket.get_page_selectors()[''])
            if product_title:
                if supermarket.attributes:
                    print(product_title.attrs[(supermarket.get_page_selectors()['attributes'])['name']])
                else:
                    print(product_title.text)
            else:
                print('Product name selector at non-existing namespace.')
            