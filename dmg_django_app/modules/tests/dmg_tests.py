import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dmg_django.settings")
django.setup()

from unittest import TestSuite, TextTestRunner, TestCase
from concurrent.futures import ThreadPoolExecutor
from ..extraction import Scraper
from ..transformation import ReceiptRenderer, query_items, receipt
from ..common import Supermarkets

class DMGTestCase(TestCase):
    """Test cases for the discount_my_groceries application."""
    
    @classmethod
    def setUp(self):
        super().setUp(self)
        self.data:dict[str] = {
            "PicknPay": {
                "Jacob's Kronung Coffee": {"total_price": "R379.98", "quantity": "2", "cost_of_item": "R189.99"},
                "Albany Brown Bread": {"total_price": "R33.98", "quantity": "2", "cost_of_item": "R16.99"},
                "No Name Potatoes Bag 1 x 1kg": {"total_price": "R78.99", "quantity": "1"},
                "Eggberts Eggs 60": {"total_price": "R258.98", "quantity": "2", "cost_of_item": "R129.99"}
            }}
    
    def headless_browser_test(self):
        scraper = Scraper()
        scraper.scrape_products([Supermarkets.SUPERMARKETS[Supermarkets.MAKRO]])

    def receipt_renderer_test(self):
        items:dict[str] = {}
        rr = ReceiptRenderer()
        q:str = input('Search item:\n>>>')
        f:str = input('\nFilter?')
        if f == 'Y' or f == 'Yes':
            s:str = input('\nType supermarket name\n>>>')
            items = query_items(query=q, supermarket_name=s, receiptify=True)
            rr.render(items, s)
        else:
            items = query_items(q, receiptify=True)
            rr.render(items)

    def models_test(self):
        q = input('Type item:\n>>>')
        print(query_items(q))

    def receiptify_test(self):
        receipt(self.data)

def map_function(func, container: list):
    with ThreadPoolExecutor() as execute:
        return execute.map(func, container)
    
def suite():
    _suite = TestSuite()
    g_test:str = '4. receiptify_test'
    m_test:str = '3. models_test'
    r_test:str = '2. receipt_renderer_test'
    h_test:str = '1. headless_browser_test'

    r = input(f'{h_test}\n{r_test}\n{m_test}\n{g_test}\n>>>')

    if r == '1':
        _suite.addTest(DMGTestCase('headless_browser_test'))
    elif r == '2':
        _suite.addTest(DMGTestCase('receipt_renderer_test'))
    elif r == '3':
        _suite.addTest(DMGTestCase('models_test'))
    elif r == '4':
        _suite.addTest(DMGTestCase('receiptify_test'))
    return _suite

if __name__ == '__main__':
    _runner = TextTestRunner(verbosity=3)
    _runner.run(suite())