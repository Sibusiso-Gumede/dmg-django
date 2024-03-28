from ..extraction import Scraper
from ..transformation import Receipt_Renderer
from concurrent.futures import ThreadPoolExecutor
from ..supermarket_apis import Woolworths, Shoprite, Makro, PicknPay, Checkers

from unittest import TestCase, TextTestRunner, TestSuite

class DMGTestCase(TestCase):
    """Test cases for the discount_my_groceries application."""
    
    def headless_browser_test(self):
        #woolies = Woolworths()
        #shoprite = Shoprite()
        pnp = PicknPay()
        #checkers = Checkers()
        #makro = Makro()
        scraper = Scraper()
        scraper.scrape_all_data([pnp])

    def receipt_renderer_test(self):
        items = {'Simba Salt and Vinegar 250g': '12.50',
                 'Sir Juice Green Machine 1L': '39.99',
                 'Mince Samoosas 5s': '50.00'}
        rr = Receipt_Renderer()
        rr.render(items=items)

def map_function(self, func, container: list):
    with ThreadPoolExecutor() as execute:
        return execute.map(func, container)
    
def suite():
    suite = TestSuite()
    suite.addTest(DMGTestCase('headless_browser_test'))
    #suite.addTest(DMGTestCase('receipt_renderer_test'))
    return suite

if __name__ == '__main__':
    runner = TextTestRunner()
    runner.run(suite())