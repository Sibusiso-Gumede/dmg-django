# A web scraping module for data extraction.
# Different functions for specific purposes.
# The scrape_searched_products function is for a web app that utilizes a search engine
# model to deliver information of the required products. However, this approach is inefficient
# in terms of processing requests/responses for some supermarket websites. It suffices to say,
# it's suitable for low demand use cases.
# On the other hand, the scrape_all_data function collects product data from all supermarkets
# and prepares it for database storage.

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from time import sleep
from supermarket_apis import Supermarket

class Scraper():
    def __init__(self, supermarkets: list[Supermarket]) -> None:
        self.__s_list = supermarkets
        
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument('--headless')
        chromeOptions.page_load_strategy = 'normal'
        
        self.__driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chromeOptions)
        self.__driver.maximize_window()

    def __del__(self):
        self.__driver.close()
        self.__driver.quit()

    def __isRelevant(self, item: str, result: str) -> bool:
        for substring in item.split('%20'):
            if (substring[1:] in result) or (result[0] == 'R' and result[-1].isdigit()) or (result[:3] == 'Buy'):
                return True
        return False

    def scrape_searched_products(self, product_name: str):        
        product_name = product_name.replace(' ', '%20')
        for supermarket in self.__s_list:
            self.__driver.get(supermarket.get_home_page_url().replace('item', product_name))
            sleep(0.5)
            products = self.__driver.find_elements(by=By.CSS_SELECTOR, value=supermarket.get_page_selectors()['product_list'])
            for product in products:
                try:
                    if product.text:
                        if supermarket.get_supermarket_name() != 'makro':
                            print(product.text)
                        elif self.__isRelevant(product_name, product.text):
                            print(product.text)
                except StaleElementReferenceException:
                    pass

    def scrape_all_data(self):
        