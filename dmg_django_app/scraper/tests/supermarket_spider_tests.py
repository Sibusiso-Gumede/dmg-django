from extraction import SparStaticSpider, parse_response, send_request
from supermarket_apis import Spar

from unittest import TestCase, TextTestRunner, TestSuite

class SupermarketSpiderTestCase(TestCase):
    """Test cases for the supermarket spiders."""
    def spar_spider_test(self):
        self.spar = Spar()
        self.spar_spider = SparStaticSpider()
        self.spar_spider.capture_data(parse_response(send_request(self.spar.products_page_url())))

def suite():
    suite = TestSuite()
    suite.addTest(SupermarketSpiderTestCase('spar_spider_test'))
    return suite

if __name__ == '__main__':
    runner = TextTestRunner()
    runner.run(suite())
