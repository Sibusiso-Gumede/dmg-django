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
        scraper = Scraper([pnp])
        scraper.scrape_all_data()

    def receipt_renderer_test(self):
        Receipt_Renderer.render()

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
