from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from time import sleep
from supermarket_apis import Supermarket

def headless_browser(supermarket: Supermarket, product_name: str):
    
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument('--headless')
    
    with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chromeOptions) as _driver:
        _driver.maximize_window()
        
        _driver.get(supermarket.get_home_page_url())
        search_bar = _driver.find_element(by=By.CSS_SELECTOR, value=supermarket.get_page_selectors()['search_bar'])
        search_bar.send_keys(product_name)
        search_bar.submit()

        # Halt for the page to load completely.
        sleep(5)

        products = _driver.find_elements(by=By.CSS_SELECTOR, value=supermarket.get_page_selectors()['product_list'])
        for product in products:
            if supermarket.text_prod_details:
                print(product.text)
            else:    
                product_title = product.find_element(by=By.CSS_SELECTOR, value=supermarket.get_page_selectors()['product_title'])
                if product_title:
                    if supermarket.attributes:
                        print(product_title.attrs[(supermarket.get_page_selectors()['attributes'])['name']])
                    else:
                        print(product_title.text)
                else:
                    print('Product name selector error.')