from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from ..supermarket_apis import Supermarket
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

class HeadlessBrowser():
    def run(supermarkets: list[Supermarket], product: str):
        
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument('--headless')
        
        with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chromeOptions) as _driver:
            _driver.maximize_window()
            
            for supermarket in supermarkets:
                _driver.get(supermarket.get_home_page_url())
                search_bar = _driver.find_element(by=By.CSS_SELECTOR, value=supermarket.get_page_selectors()['search_bar'])
                search_bar.send_keys(product)
                search_bar.submit()

                # Halt for the page to load completely.
                sleep(5)

                products = _driver.find_elements(by=By.CSS_SELECTOR, value=supermarket.get_page_selectors()['product'])
                for _product in products:
                    product_name = _product.find_element(by=By.CSS_SELECTOR, value=supermarket.get_page_selectors()['product_name'])
                    if product_name:
                        print(product_name.get_attribute('title'))