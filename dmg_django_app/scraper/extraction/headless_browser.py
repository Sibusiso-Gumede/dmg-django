from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from supermarket_apis import Supermarket
import selenium.webdriver.common.by as By

class HeadlessBrowser():
    def run_headless_browser(supermarkets: list[Supermarket], product):
        
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument('--headless')
        
        with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chromeOptions) as _driver:
            _driver.maximize_window()
            
            for supermarket in supermarkets:
                _driver.get(supermarket.get_home_page_url())
                search_bar = _driver.find_element(by=By.CSS_SELECTOR, value=supermarket.get_page_selectors()['search_bar'])
                submit_button = _driver.find_element(by=By.CSS_SELECTOR, value=supermarket.get_page_selectors()['submit_button'])

                actions = webdriver.ActionChains(_driver, 1000)
                actions.move_to_element(search_bar).send_keys_to_element(product)
                actions.click(submit_button).perform()

                products = _driver.find_elements(by=By.CSS_SELECTOR, value=supermarket.get_page_selectors['product'])
                for _product in products:
                    product_name = _product.find_element(by=By.CSS_SELECTOR, value=supermarket.get_page_selectors()['product_name']).text
                    print(product_name)