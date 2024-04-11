from ..extraction import Scraper
from ..transformation import Receipt_Renderer
from concurrent.futures import ThreadPoolExecutor
from ..transformation import serialize_data
from ..supermarket_apis import Supermarket, Woolworths, Shoprite, Makro, PicknPay, Checkers
from ...models import Supermarket, Product

from unittest import TestCase, TextTestRunner, TestSuite

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

def map_function(self, func, container: list):
    with ThreadPoolExecutor() as execute:
        return execute.map(func, container)
    
def suite():
    suite = TestSuite()
    _test_:str = '3. organize_file_data_test'
    _test:str = '2. receipt_renderer_test'
    test:str = '1. headless_browser_test'
    r = input(f'{test}\n{_test}\n{_test_}\n>>>')
    if r == '1':
        suite.addTest(DMGTestCase('headless_browser_test'))
    elif r == '2':
        suite.addTest(DMGTestCase('receipt_renderer_test'))
    elif r == '3':
        suite.addTest(DMGTestCase('organize_file_data_test'))
    return suite

if __name__ == '__main__':
    runner = TextTestRunner()
    runner.run(suite())