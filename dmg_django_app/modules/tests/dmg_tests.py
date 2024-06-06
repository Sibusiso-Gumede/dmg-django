import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dmg_django.settings")
django.setup()

from unittest import TestSuite, TextTestRunner, TestCase
from concurrent.futures import ThreadPoolExecutor
from ..extraction import Scraper
from ..transformation import ReceiptRenderer, query_items, clean_data, store_supermarket_record, store_product_records
from ..common import Supermarkets

class DMGTestCase(TestCase):
    """Test cases for the discount_my_groceries application."""
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
    
    def headless_browser_test(self):
        scraper = Scraper()
        scraper.scrape_products([Supermarkets.SUPERMARKETS[Supermarkets.MAKRO]])

    def receipt_renderer_test(self):
        items:dict[str] = {}
        rr = ReceiptRenderer()
        q:str = input('Search item:\n>>>')
        r:str = input('\nFilter?')
        if r == 'Y':
            s:str = input('\nType supermarket name\n>>>')
            items = query_items(q, s, True)
            rr.render(items, s)
        else:
            items = query_items(q)
            rr.render(items)

    def models_test(self):
        query_items('Nescafe')

def map_function(func, container: list):
    with ThreadPoolExecutor() as execute:
        return execute.map(func, container)
    
def suite():
    _suite = TestSuite()
    m_test:str = '3. models_test'
    r_test:str = '2. receipt_renderer_test'
    h_test:str = '1. headless_browser_test'

    r = input(f'{h_test}\n{r_test}\n{m_test}\n>>>')

    if r == '1':
        _suite.addTest(DMGTestCase('headless_browser_test'))
    elif r == '2':
        _suite.addTest(DMGTestCase('receipt_renderer_test'))
    elif r == '3':
        _suite.addTest(DMGTestCase('models_test'))
    return _suite

if __name__ == '__main__':
    _runner = TextTestRunner(verbosity=3)
    _runner.run(suite())