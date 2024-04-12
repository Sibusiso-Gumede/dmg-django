# The extraction component of the ETL pipeline.
# The scrape_products method collects product data from all supermarkets
# and prepares it for database storage.

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains, KeyInput, PointerInput, WheelInput
from selenium.webdriver.common.actions.interaction import POINTER_MOUSE, KEY, WHEEL
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from time import sleep
from random import choice
from ..supermarket_apis import Supermarket
from ..common import SupermarketNames
from os import path, makedirs
import json, traceback

class Scraper():
    
    def __init__(self) -> None:
        self.chromeOptions = webdriver.ChromeOptions()
        #self.chromeOptions.add_argument('--headless')
        self.chromeOptions.add_argument('--no-sandbox')
        self.chromeOptions.page_load_strategy = 'normal'
        
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=self.chromeOptions)
        self.driver.set_window_size(1351, 598)
        self.driver.maximize_window()
        self.actions = ActionChains(self.driver, devices=[WheelInput(WHEEL), PointerInput(POINTER_MOUSE,POINTER_MOUSE), KeyInput(KEY)])
        self.WAITING_TIME_RANGE = range(1, 3)

    def _isRelevant(self, item: str, result: str) -> bool:
        for substring in item.split('%20'):
            if (substring[1:] in result) or (result[0] == 'R' and result[-1].isdigit()) or (result[:3] == 'Buy'):
                return True
        return False

    def _update_product_list(self, _super: Supermarket, product_list: dict[str]):
        print('\nSCRAPING PRODUCT LIST...')
        products = self.driver.find_elements(by=By.CSS_SELECTOR, value=_super.get_page_selectors()['product_list'])
        name: str = None
        promo: str = None
        price: str = None
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
                if (_super.get_supermarket_name() == SupermarketNames.PNP) and (prod_name_exception):
                    name = name_element.get_attribute("data-cnstrc-item-name")
                else:
                    name = name_element.text
                    
                price = price_element.text
                if _super.get_supermarket_name() == SupermarketNames.MAKRO:
                    price = f'{price[:-2]}.{price[-2:]}'
                
                if promo_element is not None:
                    if (_super.get_supermarket_name() == SupermarketNames.MAKRO) and ('for' not in promo_element.text):
                        promo = "NULL"
                    else:
                        promo = promo_element.text
                elif promo_element is None:
                    promo = "NULL"
                _super.increase_product_count()
                product_list.update({_super.get_product_count(): {"name": name, "price": price, "promo": promo}})    
        print("DONE.")

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

    def _prepare_url_patterns(self, _supermarket: Supermarket) -> bool:
        # Read data and return complete url's.
        s_name = _supermarket.get_supermarket_name()
        resources_dir = f'{_supermarket.RESOURCES_PATH}/{s_name}'
        output_file = f'{resources_dir}/{s_name}_urls.txt'
        if not path.isfile(output_file):
            input_file = f'{resources_dir}/{s_name}_categories.json'
            urls: list[str] = list()
            url: str
            with open(input_file, 'r') as  i_file, open(output_file, 'x', newline='\n') as urls_file:
                categories = dict(json.load(i_file))                
                for category, data in zip(categories.keys(), categories.values()):
                    if s_name == SupermarketNames.MAKRO:
                        for subcategory, _attributes in zip(data.keys(), data.values()):
                            url = _supermarket.get_category_page_url()
                            url = url.replace("category", category).replace("sub", subcategory).replace("idcode", _attributes['ID'])
                            urls.append(url+'\n')
                    elif s_name == SupermarketNames.WOOLIES:
                        url = _supermarket.get_category_page_url()
                        url = url.replace("category", category).replace('idcode', data['ID'])
                        urls.append(url+'\n')
                urls_file.writelines(urls)
            return path.isfile(output_file)
        else:
            return True
        
    def _retrieve_urls(self, _supermarket: Supermarket) -> list[str]:
        urls_file = f'{_supermarket.RESOURCES_PATH}/{_supermarket.get_supermarket_name()}/{_supermarket.get_supermarket_name()}_urls.txt'
        with open(urls_file, 'rt', newline='\n') as file:
            urls: list[str] = list()
            for line in file.readlines():
                urls.append(line.removesuffix('\n'))
            return urls
           
    def scrape_products(self, supermarkets: list[Supermarket]):
        divisor_range: list[int] = range(2, 6)       
        url_count: int = 0
        urls = list[str]
        next_button: WebElement
        home_page: bool
        makro_subcategory_products_loaded: bool = False
        last_page: int = 0
        supermarket_name: str
        #script:str = r'window.scroll({top:550,left:0,behavior:"smooth",});'

        for supermarket in supermarkets:
            home_page = True
            page_number:int = 0
            supermarket_name = supermarket.get_supermarket_name()
            sleep(1.50)
            buffer: dict[str] = {}

            if ((supermarket_name == SupermarketNames.WOOLIES) or (supermarket_name == SupermarketNames.MAKRO)) and (self._prepare_url_patterns(supermarket)):
                urls = self._retrieve_urls(supermarket)
                url_count = len(urls)
            
            while True:
                #if not (supermarket_name == SupermarketNames.MAKRO):
                page_number += 1

                if home_page:
                    if (supermarket_name == SupermarketNames.WOOLIES) or (supermarket_name == SupermarketNames.MAKRO):
                        self.driver.get(urls[url_count-1])
                        url_count -= 1
                    elif not (supermarket_name == SupermarketNames.WOOLIES):
                        if not (supermarket_name == SupermarketNames.MAKRO):
                            self.driver.get(supermarket.get_home_page_url())
                        if not ((supermarket_name == SupermarketNames.PNP) or (supermarket_name == SupermarketNames.MAKRO)):
                            self.driver.find_element(by=By.CSS_SELECTOR, value=supermarket.get_page_selectors()['browse_nav']).click()
                        elif (supermarket_name == SupermarketNames.PNP) or (supermarket_name == SupermarketNames.MAKRO):
                            if supermarket_name == SupermarketNames.MAKRO:
                                # Move the focus to the body segment of the page.
                                self.driver.execute_script("arguments[0].click();",
                                                           self.driver.find_element(By.CSS_SELECTOR, supermarket.get_page_selectors()['body']))
                            # Scroll to the bottom of the page.
                            self.actions.scroll_by_amount(0, 550)
                            sleep(5)
                            for y in range(0, 8):
                                self.actions.perform()
                            sleep(5)
                            self.actions.reset_actions()
                            if supermarket_name == SupermarketNames.PNP:
                                href: str = self.driver.find_element(By.CSS_SELECTOR, 
                                                                     supermarket.get_page_selectors()['last_page_button']).get_dom_attribute('href')
                                last_page = int((href[href.find('='):])[1:])
                    home_page = False
                elif not home_page:
                    selector:str = supermarket.get_page_selectors()['next_button']
                    if supermarket_name == SupermarketNames.PNP:
                        if page_number <= last_page:
                            selector = selector.replace('number', f'{page_number}')
                        elif page_number > last_page:
                            break
                                                
                    # Click to the next page if it's available.
                    next_button = self.driver.find_element(by=By.CSS_SELECTOR, value=selector)                

                    # In the case where there are still products to be scraped, load the next page.
                    if next_button.is_enabled():
                        self.driver.execute_script("arguments[0].click();", next_button)
                        
                        if (supermarket_name == SupermarketNames.PNP) or (supermarket_name == SupermarketNames.MAKRO):
                            self.actions.scroll_by_amount(0, 550)
                            sleep(5)
                            for y in range(0, 8):
                                self.actions.perform()
                            sleep(5)
                            self.actions.reset_actions()
                            breakpoint()
                    # Otherwise, if the final page of the products is reached, proceed to the next supermarket website.
                    elif not next_button.is_enabled():
                        if ((supermarket_name == SupermarketNames.SHOPRITE) or (supermarket_name == SupermarketNames.CHECKERS)) or (((supermarket_name == SupermarketNames.WOOLIES) or (supermarket_name == SupermarketNames.MAKRO)) and (url_count == -1)):
                            print(f'Available items completely scraped for {supermarket_name} website.')
                            break
                        # Proceed to the next category if the items are completely scraped for the current category.
                        elif ((supermarket_name == SupermarketNames.WOOLIES) or (supermarket_name == SupermarketNames.MAKRO)) and (url_count > -1):
                            home_page = True
                            if supermarket_name == SupermarketNames.MAKRO:
                                makro_subcategory_products_loaded = True

                sleep((choice(self.WAITING_TIME_RANGE))/(choice(divisor_range)))

                # Update product list.
                if not (supermarket_name == SupermarketNames.MAKRO):
                    print(f"\nPAGE {page_number} OF {supermarket_name}")
                    self._update_product_list(supermarket, buffer)
                    if page_number == 2:
                        break
                elif (supermarket_name == SupermarketNames.MAKRO) and (page_number == 2):#(makro_subcategory_products_loaded):
                    self._update_product_list(supermarket, buffer)
                    #makro_subcategory_products_loaded = False
                    break
                
            # Populate supermarket database fixtures.
            self._populate_fixtures(supermarket, buffer)