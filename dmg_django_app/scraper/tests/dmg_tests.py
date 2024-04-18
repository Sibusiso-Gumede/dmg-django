from django.test import TestCase, runner
from concurrent.futures import ThreadPoolExecutor
from ..extraction import Scraper
from ..transformation import Receipt_Renderer, store_supermarket_record, store_product_records
from ..common import Supermarkets

class DMGTestCase(TestCase):
    """Test cases for the discount_my_groceries application."""
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.supermarkets = Supermarkets()

    def tearDown(self) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass
    
    def headless_browser_test(self):
        scraper = Scraper()
        scraper.scrape_products([self.supermarkets[self.supermarkets.MAKRO]])

    def receipt_renderer_test(self):
        items = {'Simba Salt and Vinegar 250g': '12.50',
                 'Sir Juice Green Machine 1L': '39.99',
                 'Mince Samoosas 5s': '50.00'}
        rr = Receipt_Renderer()
        rr.render(items=items)

    def models_test(self):
        for name, supermarket in self.supermarkets.SUPERMARKETS.items():
            _file = open(f'{supermarket.RESOURCES_PATH}/{name}/{name}_products.json','r')                
            _products = store_supermarket_record(supermarket, _file)   
            store_product_records(name, _products)
            _file.close()

def map_function(self, func, container: list):
    with ThreadPoolExecutor() as execute:
        return execute.map(func, container)
    
def suite():
    m_test:str = '3. models_test'
    r_test:str = '2. receipt_renderer_test'
    h_test:str = '1. headless_browser_test'

    r = input(f'{h_test}\n{r_test}\n{m_test}\n>>>')
    module_class_dir:str = 'dmg_django_app.scraper.tests.dmg_tests.DMGTestCase.'
    _suite:list = []
    if r == '1':
        _suite.append(f'{module_class_dir}headless_browser_test')
    elif r == '2':
        _suite.append(f'{module_class_dir}receipt_renderer_test')
    elif r == '3':
        _suite.append(f'{module_class_dir}models_test')
    return _suite

if __name__ == '__main__':
    import os
    import django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dmg_django.settings")
    django.setup()
    _runner = runner.DiscoverRunner(keepdb=True)
    _runner.run_suite(_runner.build_suite(suite()))