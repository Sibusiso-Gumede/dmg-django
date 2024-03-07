from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from time import sleep
from supermarket_apis import Supermarket

def isRelevant(item: str, result: str) -> bool:
        for substring in item.split('%20'):
            if (substring[2:] in result) or (result[0] == 'R' and result[-1].isdigit()) or (result[:3] == 'Buy'):
                return True
        return False

def headless_browser(supermarkets: list[Supermarket], product_name: str):
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument('--headless')
    chromeOptions.page_load_strategy = 'normal'
    
    with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chromeOptions) as _driver:
        _driver.maximize_window()
        
        product_name = product_name.replace(' ', '%20')
        for supermarket in supermarkets:
            _driver.get(supermarket.get_home_page_url().replace('item', product_name))
            sleep(0.5)
            products = _driver.find_elements(by=By.CSS_SELECTOR, value=supermarket.get_page_selectors()['product_list'])
            for product in products:
                try:
                    if product.text:
                        if supermarket.get_supermarket_name() != 'makro':
                            print(product.text)
                        elif isRelevant(product_name, product.text):
                            print(product.text)
                except StaleElementReferenceException:
                    pass