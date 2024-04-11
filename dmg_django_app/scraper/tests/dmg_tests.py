from django.test import TestCase, runner

from ..extraction import Scraper
from ..transformation import Receipt_Renderer
from concurrent.futures import ThreadPoolExecutor
from ..transformation import serialize_data
from ..supermarket_apis import Supermarket, Woolworths, Shoprite, Makro, PicknPay, Checkers
from ...models import Supermarket, Product

class DMGTestCase(TestCase):
    """Test cases for the discount_my_groceries application."""
    def __init__(self):
        self.supermarkets = {
        "woolies": Woolworths(),
        "shoprite": Shoprite(),
        "pnp": PicknPay(),
        "checkers": Checkers(),
        "makro": Makro()
        }

    def headless_browser_test(self):
        scraper = Scraper()
        scraper.scrape_products([self.supermarkets["makro"]])

    def receipt_renderer_test(self):
        items = {'Simba Salt and Vinegar 250g': '12.50',
                 'Sir Juice Green Machine 1L': '39.99',
                 'Mince Samoosas 5s': '50.00'}
        rr = Receipt_Renderer()
        rr.render(items=items)
    
    def serialize_data_test(self):
        for supermarket in self.supermarkets.values():
            serialize_data(s=supermarket)

    def add_supermarket_models_test(self):
        for s in self.supermarkets.values():
            obj = Supermarket()

def map_function(self, func, container: list):
    with ThreadPoolExecutor() as execute:
        return execute.map(func, container)
    
def suite():
    a_test:str = '4. add_supermarket_models_test'
    o_test:str = '3. organize_file_data_test'
    r_test:str = '2. receipt_renderer_test'
    h_test:str = '1. headless_browser_test'

    r = input(f'{h_test}\n{r_test}\n{o_test}\n{a_test}\n>>>')
    _suite:list = []
    if r == '1':
        _suite.append('DMGTestCase.headless_browser_test')
    elif r == '2':
        _suite.append('DMGTestCase.receipt_renderer_test')
    elif r == '3':
        _suite.append('DMGTestCase.organize_file_data_test')
    return _suite

if __name__ == '__main__':
    _runner = runner.DiscoverRunner(keepdb=True)
    _runner.run_suite(_runner.build_suite(suite()))