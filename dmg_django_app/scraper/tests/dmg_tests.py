from django.test import TestCase, runner
from concurrent.futures import ThreadPoolExecutor
from ..extraction import Scraper
from ..supermarket_apis import Woolworths, Shoprite, Makro, PicknPay, Checkers
from ..common import SupermarketNames

class DMGTestCase(TestCase):
    """Test cases for the discount_my_groceries application."""
    def __init__(self):
        self.supermarkets = {
        SupermarketNames.WOOLIES: Woolworths(),
        SupermarketNames.SHOPRITE: Shoprite(),
        SupermarketNames.PNP: PicknPay(),
        SupermarketNames.CHECKERS: Checkers(),
        SupermarketNames.MAKRO: Makro()
        }

    def headless_browser_test(self):
        scraper = Scraper()
        scraper.scrape_products([self.supermarkets[SupermarketNames.MAKRO]])

    def receipt_renderer_test(self):
        items = {'Simba Salt and Vinegar 250g': '12.50',
                 'Sir Juice Green Machine 1L': '39.99',
                 'Mince Samoosas 5s': '50.00'}
        rr = Receipt_Renderer()
        rr.render(items=items)

    def models_test(self):
        for name, supermarket in self.supermarkets.items():   
            store_product_records(name, store_supermarket_records(supermarket))

def map_function(self, func, container: list):
    with ThreadPoolExecutor() as execute:
        return execute.map(func, container)
    
def suite():

    m_test:str = '3. models_test'
    r_test:str = '2. receipt_renderer_test'
    h_test:str = '1. headless_browser_test'

    r = input(f'{h_test}\n{r_test}\n{m_test}\n>>>')
    _suite:list = []
    if r == '1':
        _suite.append('DMGTestCase.headless_browser_test')
    elif r == '2':
        _suite.append('DMGTestCase.receipt_renderer_test')
    elif r == '3':
        suite.append('DMGTestCase.supermarket_models_test')
    return _suite

if __name__ == '__main__':
    import django
    django.setup()
    from ..transformation import Receipt_Renderer, store_supermarket_records, store_product_records
    _runner = runner.DiscoverRunner(keepdb=True)
    _runner.run_suite(_runner.build_suite(suite()))