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
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from time import sleep
from random import choice
from ..supermarket_apis import Supermarket
from os import path, makedirs
import json, traceback

class Scraper():
    PNP = 'picknpay'
    WOOLIES = 'woolworths'
    SHOPRITE = 'shoprite'
    CHECKERS = 'checkers'
    MAKRO = 'makro'
    
    def __init__(self) -> None:
        self.chromeOptions = webdriver.ChromeOptions()
        self.chromeOptions.add_argument('--headless')
        self.chromeOptions.add_argument('--no-sandbox')
        self.chromeOptions.page_load_strategy = 'normal'
        
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=self.chromeOptions)
        self.driver.set_window_size(1351, 598)
        self.driver.maximize_window()
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

    def _update_product_list(self, _super: Supermarket, product_list: dict[str]):
        print('\nPRODUCT LIST...\n')
        products = self.driver.find_elements(by=By.CSS_SELECTOR, value=_super.get_page_selectors()['product_list'])
        name: str = None
        prod_name_exception: bool = False
        name_element: WebElement = None
        price_element: WebElement = None
        promo_element: WebElement = None
        for product in products:
            try:    
                name_element = product.find_element(by=By.CSS_SELECTOR, value=_super.get_page_selectors()['product_name'])
                price_element = product.find_element(by=By.CSS_SELECTOR, value=_super.get_page_selectors()['product_price'])
                promo_element = product.find_element(by=By.CSS_SELECTOR, value=_super.get_page_selectors()['product_promo'])
            except NoSuchElementException as error:
                line = traceback.format_exception_only(error)[0]
                if _super.get_page_selectors()['product_name'] in line:
                    name_element = product.find_element(by=By.CSS_SELECTOR, value=_super.get_page_selectors()['product_name_alternative'])
                    prod_name_exception = True
                elif _super.get_page_selectors()['product_price'] in line:
                    price_element = None
                elif _super.get_page_selectors()['product_promo'] in line:
                    promo_element = None
            finally:
                if (_super.get_supermarket_name() == self.PNP) and (prod_name_exception):
                    name = name_element.get_attribute("data-cnstrc-item-name")
                else:
                    name = name_element.text

                if promo_element is not None:
                    product_list.update({name: {"price": price_element.text, "promo": promo_element.text}})
                elif promo_element is None:
                    product_list.update({name: {"price": price_element.text, "promo": "NULL"}})
                elif price_element is None:
                    product_list.update({name: {"price": "NULL", "promo": "NULL"}})

    def _populate_fixtures(self, _supermarket: Supermarket, products: dict[str]):
        # Populate database fixtures. 
        output_dir = f'{_supermarket.RESOURCES_PATH}/{_supermarket.get_supermarket_name()}'
        output_file = f'{output_dir}/{_supermarket.get_supermarket_name()}_products.json'
        arg = 'w'               # open file in write mode.
        if not path.isdir(output_dir):
            makedirs(output_dir)
        if not path.isfile(output_file):
            arg = 'x'           # create file and open in write mode.
        with open(output_file, arg) as o_file:
            json.dump(products, o_file, indent=4)

    def _prepare_url_patterns(self, _supermarket: Supermarket) -> list[str]:
        # Read data and return complete url's.
        input_file = f'{_supermarket.RESOURCES_PATH}/{_supermarket.get_supermarket_name()}/categories.json'
        urls = list()
        with open(input_file, 'r') as i_file:
            categories = dict(json.load(i_file))
            for name, id in zip(categories.keys(), categories.values()):
                url = _supermarket.get_query_page_url().replace('name', name).replace('idcode', id['ID'])
                urls.append(url)
        return urls

    def _capture_products(self, supermarkets: list[Supermarket]):
        divisor_range: list[int] = range(2, 6)       
        url_count: int = 0
        urls = list[str]
        next_button: WebElement
        home_page: bool
        last_page: int = 0
        supermarket_name: str
        script:str = r'window.scroll({top:550,left:0,behavior:"smooth",});'

        for supermarket in supermarkets:
            home_page = True
            page_number = 0
            supermarket_name = supermarket.get_supermarket_name()
            sleep(1.50)
            buffer: dict[str] = {}

            if supermarket_name == self.WOOLIES:
                urls = self._prepare_url_patterns(supermarket)
                url_count = len(urls)

            while True:
                page_number += 1
                if home_page:
                    if not (supermarket_name == self.WOOLIES):
                        self.driver.get(supermarket.get_home_page_url())
                        if not (supermarket_name == self.PNP):
                            self.driver.find_element(by=By.CSS_SELECTOR, value=supermarket.get_page_selectors()['browse_nav']).click()
                        elif supermarket_name == self.PNP:
                            # Scroll to the bottom of the page.
                            sleep(5)
                            for y in range(0, 8):
                                self.driver.execute_script(script=script)
                            sleep(5)
                            href: str = self.driver.find_element(by=By.CSS_SELECTOR, value=supermarket.get_page_selectors()['last_page_button']).get_dom_attribute('href')
                            last_page = int((href[href.find('='):])[1:])
                    elif supermarket_name == self.WOOLIES:
                        self.driver.get(urls[url_count-1])
                        url_count -= 1
                    home_page = False
                elif not home_page:
                    selector:str = supermarket.get_page_selectors()['next_button']
                    if supermarket_name == self.PNP:
                        if page_number <= last_page:
                            selector = selector.replace('number', f'{page_number}')
                        elif page_number > last_page:
                            break
                            
                    # Click to the next page if it's available.
                    next_button = self.driver.find_element(by=By.CSS_SELECTOR, value=selector)                
                    
                    # In the case where there are still products to be scraped, load the next page.
                    if next_button.is_enabled():
                        self.driver.execute_script("arguments[0].click();", next_button)
                        if supermarket_name == self.PNP:
                            sleep(5)
                            for y in range(0, 8):
                                self.driver.execute_script(script=script)
                            sleep(5)
                    # Otherwise, if the final page of the products is reached, proceed to the next supermarket website.
                    elif not next_button.is_enabled():
                        if ((supermarket_name == self.SHOPRITE) or (supermarket_name == self.CHECKERS)) or ((supermarket_name == self.WOOLIES) and (url_count == -1)):
                            print(f'Available items completely scraped for {supermarket_name} website.')
                            break
                        # Proceed to the next category if the items are completely scraped for the current category.
                        elif (supermarket_name == self.WOOLIES) and (url_count > -1):
                            home_page = True
                
                sleep((choice(self.WAITING_TIME_RANGE))/(choice(divisor_range)))
                print(f"\nPAGE {page_number} OF {supermarket_name}")
                self._update_product_list(supermarket, buffer)
                
                if page_number == 2:
                    break
                
            # Populate supermarket database fixtures.
            self._populate_fixtures(supermarket, buffer)