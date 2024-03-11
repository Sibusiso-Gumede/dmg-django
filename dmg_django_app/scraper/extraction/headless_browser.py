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
from random import choice
from ..supermarket_apis import Supermarket

class Scraper():
    def __init__(self, supermarkets: list[Supermarket]) -> None:
        self.__s_list = supermarkets
        
        self.__chromeOptions = webdriver.ChromeOptions()
        self.__chromeOptions.add_argument('--headless')
        self.__chromeOptions.page_load_strategy = 'normal'
        
        self.__driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=self.__chromeOptions)
        self.__driver.maximize_window()
        self.__WAITING_TIME_RANGE = range(1, 3)
        self.__SEARCHED_PRODUCTS = 'searched products'
        self.__ALL_DATA = 'all data'
        self.__mode = str()

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
        self.__mode = self.__SEARCHED_PRODUCTS
        self.__capture_products()

    def scrape_all_data(self):
        self.__mode = self.__ALL_DATA
        self.__capture_products()

    def __capture_products(self, product_name: str = None):
        divisor_range = range(2, 6)

        def product_list(super: Supermarket):
            selectors = super.get_page_selectors()
            products = self.__driver.find_elements(by=By.CSS_SELECTOR, value=selectors['product_list'])
            for product in products:
                try:
                    prod_name = product.find_element(by=By.CSS_SELECTOR, value=selectors['product_name'])
                    prod_price = product.find_element(by=By.CSS_SELECTOR, value=selectors['product_price'])
                    prod_pomo = product.find_element(by=By.CSS_SELECTOR, value=selectors['product_promo'])
                    if prod_name and prod_price:
                        if supermarket.get_supermarket_name() != 'makro':
                            print(f"{prod_name.text}\n{prod_price}")
                            if prod_pomo:
                                print(f'\n{prod_pomo.text}')
                        elif self.__isRelevant(product_name, product.text):
                            print(product.text)
                    else:
                        print('Product Name or Product Price Not Found.')
                except StaleElementReferenceException:
                    pass
        
        for supermarket in self.__s_list:
            selectors = supermarket.get_page_selectors()
            if self.__mode == self.__ALL_DATA:
                self.__driver.get(supermarket.get_home_page_url())
                page = 1
                sleep(0.5)
                self.__driver.find_element(by=By.CSS_SELECTOR, value=supermarket.get_page_selectors()['browse_nav']).click()
                sleep(0.65)
                print(f"PAGE 1 OF {supermarket.get_supermarket_name()}")
                product_list(super=supermarket)
                next_button = self.__driver.find_element(by=By.CSS_SELECTOR, value=supermarket.get_page_selectors()['next_button'])
                while next_button.is_enabled():
                    next_button.click()
                    page += 1
                    sleep((choice(self.__WAITING_TIME_RANGE))/(choice(divisor_range)))
                    print(f"\nPAGE {page} OF {supermarket.get_supermarket_name()}")
                    product_list(super=supermarket)
                    breakpoint()
                    next_button = self.__driver.find_element(by=By.CSS_SELECTOR, value=supermarket.get_page_selectors()['next_button'])

            elif self.__mode == self.__SEARCHED_PRODUCTS:
                self.__driver.get(supermarket.get_query_page_url().replace('item', self.__options['product_name']))
                sleep(0.7)