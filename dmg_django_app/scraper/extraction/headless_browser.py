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
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions.wheel_input import WheelInput
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.actions.interaction import *
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from time import sleep
from random import choice
from ..supermarket_apis import Supermarket
from os import path, makedirs
import json

class Scraper():
    PNP = 'picknpay'
    WOOLIES = 'woolworths'
    SHOPRITE = 'shoprite'
    CHECKERS = 'checkers'
    MAKRO = 'makro'
    
    def __init__(self) -> None:
        self.chromeOptions = webdriver.ChromeOptions()
        self.chromeOptions.add_argument('--headless')
        self.chromeOptions.page_load_strategy = 'normal'
        
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=self.chromeOptions)
        self.driver.set_window_size(1351, 598)
        self.driver.maximize_window()
        self.mouse_wheel = WheelInput('MouseWheel')
        self.mouse_pointer = PointerInput(POINTER_MOUSE,'MousePointer')
        self.actions = ActionChains(self.driver, 500, [self.mouse_pointer, self.mouse_wheel])
        self.WAITING_TIME_RANGE = range(1, 3)
        self.SEARCHED_PRODUCTS = 'searched products'
        self.ALL_DATA = 'all data'
        self.mode = str()

    def _isRelevant(self, item: str, result: str) -> bool:
        for substring in item.split('%20'):
            if (substring[1:] in result) or (result[0] == 'R' and result[-1].isdigit()) or (result[:3] == 'Buy'):
                return True
        return False

    def scrape_searched_products(self, product_name: str):        
        product_name = product_name.replace(' ', '%20')
        self.mode = self.SEARCHED_PRODUCTS
        self._capture_products()

    def scrape_all_data(self,  supermarkets: list[Supermarket]):
        self.mode = self.ALL_DATA
        self._capture_products(supermarkets)

    def _product_list(self, _super: Supermarket, page: int = None):
        print('\nPRODUCT LIST...\n')
        products = self.driver.find_elements(by=By.CSS_SELECTOR, value=_super.get_page_selectors()['product_list'])
        for product in products:
            prod_name = product.find_element(by=By.CSS_SELECTOR, value=_super.get_page_selectors()['product_name'])
            prod_price = product.find_element(by=By.CSS_SELECTOR, value=_super.get_page_selectors()['product_price'])
            try:
                prod_pomo = product.find_element(by=By.CSS_SELECTOR, value=_super.get_page_selectors()['product_promo'])
            except NoSuchElementException:
                prod_pomo = None
            if prod_name is not None and prod_price is not None:
                if _super.get_supermarket_name() != self.MAKRO:
                    print(prod_name.text+'\n'+prod_price.text)
                    if prod_pomo is not None:
                        print('\n'+prod_pomo.text)
            else:
                print('Product Name or Product Price Not Found.') 

    def _populate_fixtures(self, _supermarket: Supermarket, products: dict):
        # Populate database fixtures. 
        output_file = f'{_supermarket.RESOURCES_PATH}/{_supermarket.get_supermarket_name()}/{_supermarket.get_supermarket_name()}_products.json'
        if not path.isfile(output_file):
            makedirs(output_file)
        with open(output_file, 'w') as o_file:
            json.dump(products, o_file)

    def _prepare_url_patterns(self, _supermarket: Supermarket) -> list[str]:
        # Read data and return complete url's.
        input_file = f'{_supermarket.RESOURCES_PATH}/{_supermarket.get_supermarket_name()}/categories.json'
        if not path.isfile(input_file):
            makedirs(input_file)
        urls = list()
        with open(input_file, 'r') as i_file:
            categories = dict(json.load(i_file))
            for name, id in zip(categories.keys(), categories.values()):
                url = _supermarket.get_query_page_url().replace('name', name)
                url = url.replace('idcode', id['ID'])
                urls.append(url)
        return urls    

    def _scroll_to_bottom_and_top(self, _super: Supermarket):
        # Scroll to the bottom of the page and back to the top.
        self.actions.scroll_to_element(self.driver.find_element(by=By.CSS_SELECTOR, value=_super.get_page_selectors()['footer']))
        self.actions.perform()
        self.actions.reset_actions()
        self.actions.scroll_to_element(self.driver.find_element(by=By.CSS_SELECTOR, value=_super.get_page_selectors()['header']))
        self.actions.perform()
        self.actions.reset_actions()

    def _capture_products(self, supermarkets: list[Supermarket]):
        divisor_range = range(2, 6)       
        page_number = 0
        url_count = 0
        urls: list[str]
        next_button: WebElement
        home_page: bool

        for supermarket in supermarkets:
            home_page = True
        
            if supermarket.get_supermarket_name() == self.WOOLIES:
                urls = self._prepare_url_patterns(supermarket)
                url_count = len(urls)

            while True:
                if supermarket.get_supermarket_name() == self.CHECKERS or supermarket.get_supermarket_name() == self.SHOPRITE:
                    if home_page:
                        self.driver.get(supermarket.get_home_page_url())
                        self.driver.find_element(by=By.CSS_SELECTOR, value=supermarket.get_page_selectors()['browse_nav']).click()
                        home_page = False
                    elif not home_page:
                        next_button = self.driver.find_element(by=By.CSS_SELECTOR, value=supermarket.get_page_selectors()['next_button'])                
                        # In the case where there are still products to be scraped, load the next page.
                        if next_button.is_enabled():
                            next_button.click()
                        # Otherwise, stop and proceed to the next supermarket website.
                        elif not next_button.is_enabled():
                            print(f'Found items completely scraped for {supermarket.get_supermarket_name()} website.')
                            break
                elif supermarket.get_supermarket_name() == self.PNP:
                    self.driver.get(supermarket.get_home_page_url()+f'?currentPage={page_number}')
                    self._scroll_to_bottom_and_top(supermarket)
                    if self.driver.find_element(by=By.CSS_SELECTOR, value=supermarket.get_page_selectors()['products_found']).text == '(0)':
                        break 
                elif supermarket.get_supermarket_name() == self.WOOLIES:
                    if home_page:
                        self.driver.get(urls[url_count-1])
                        url_count -= 1
                        home_page = False
                    elif not home_page:
                        # TODO: fix next_button issue.
                        next_button = self.driver.find_element(by=By.CSS_SELECTOR, value=supermarket.get_page_selectors()['next_button'])
                        if next_button.is_enabled():
                            next_button.click()
                        # Continue to the next category if the last page of the current category is reached.    
                        elif (not next_button.is_enabled()) and (url_count > -1):
                            home_page = True
                            continue
                        # If the final page of the last category is reached, then proceed to the next supermarket website.
                        elif (not next_button.is_enabled()) and (url_count == -1):
                            print(f'Found items completely scraped for {supermarket.get_supermarket_name()} website.')
                            break
                page_number += 1
                sleep((choice(self.WAITING_TIME_RANGE))/(choice(divisor_range)))
                print(f"\nPAGE {page_number} OF {supermarket.get_supermarket_name()}")
                self._product_list(_super=supermarket, page=page_number)
                if page_number == 2:
                        break