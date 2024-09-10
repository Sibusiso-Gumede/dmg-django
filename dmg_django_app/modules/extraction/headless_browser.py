# The extraction component of the ETL pipeline.
# The scrape_products method collects product data from all supermarkets
# and prepares it for database storage.

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from time import sleep
from random import choice
from ..supermarket_apis import BaseSupermarket
from ..common import Supermarkets
from os import path, listdir
from sys import exit
import json, traceback

class Scraper():
    def __init__(self, s: BaseSupermarket) -> None:
        self.chromeOptions = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.geolocation" :2}
        self.chromeOptions.add_experimental_option('prefs', prefs)
        #self.chromeOptions.add_argument('--headless')
        self.chromeOptions.add_argument('--no-sandbox')
        self.chromeOptions.page_load_strategy = 'normal'
 
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=self.chromeOptions)
        self.driver.set_window_size(1351, 598)
        self.driver.maximize_window()

        self.supermarket = s
        self.supermarket_name: str = s.get_supermarket_name()
        self.url_count: int = 0
        self.urls = list[str]

        self.last_product: WebElement = None
        self.home_page: bool = True
        self.products_list: dict[str] = {}
        self.product_images = []

    def _isRelevant(self, item: str, result: str) -> bool:
        for substring in item.split('%20'):
            if (substring[1:] in result) or (result[0] == 'R' and result[-1].isdigit()) or (result[:3] == 'Buy'):
                return True
        return False

    def __update_products_list(self):
        print('\nScraping product list', end="...")

        if (self.supermarket_name == Supermarkets.CHECKERS) or (self.supermarket_name == Supermarkets.SHOPRITE):
            self.driver.execute_script(f"""document.querySelector('main[data-currency-iso-code="ZAR"] > header.header.js-mainHeader').remove();""")                         
            sleep(5)

        products = self.driver.find_elements(by=By.CSS_SELECTOR, value=self.supermarket.get_page_selectors()['product_list'])
        name: str = ""
        promo: str = ""
        price: str = ""
        image: str = ""
        prod_count: int = 0
        name_element: WebElement = None
        price_element: WebElement = None
        promo_element: WebElement = None
        image_element: WebElement = None

        if (self.supermarket_name == Supermarkets.MAKRO) and (not self.home_page) and self.last_product:
            products = products[products.index(self.last_product)+1:]

        for product in products:
            prod_count += 1
            try:    
                name_element = product.find_element(by=By.CSS_SELECTOR, value=self.supermarket.get_page_selectors()['product_name'])
                price_element = product.find_element(by=By.CSS_SELECTOR, value=self.supermarket.get_page_selectors()['product_price'])
                promo_element = product.find_element(by=By.CSS_SELECTOR, value=self.supermarket.get_page_selectors()['product_promo'])
                image_element = product.find_element(by=By.CSS_SELECTOR, value=self.supermarket.get_page_selectors()['product_image'])
            except NoSuchElementException as error:
                line = traceback.format_exception_only(error)[0]
                if self.supermarket.get_page_selectors()['product_name'] in line:
                    name_element = product.find_element(by=By.CSS_SELECTOR, value=self.supermarket.get_page_selectors()['alternative_product_name'])
                    res = input('Product name not found. Continue execution?')
                    if res != 'y':
                        exit('Scraping terminated.')
                    if (self.supermarket_name == Supermarkets.PNP):
                        name = name_element.get_dom_attribute("data-cnstrc-item-name")
                    elif (self.supermarket_name == Supermarkets.WOOLIES):
                        continue
                elif self.supermarket.get_page_selectors()['product_price'] in line:
                    price_element = None
                elif self.supermarket.get_page_selectors()['product_promo'] in line:
                    promo_element = None
                elif self.supermarket.get_page_selectors()['product_image'] in line:
                    image_element = None
                    print("Product image not visible.")
            finally:
                name = name_element.text
                
                if '/' in name:
                    name = name.replace('/', '')

                if (price_element is None) and (self.supermarket_name == Supermarkets.WOOLIES):
                    continue
                else:
                    price = price_element.text
                if self.supermarket_name == Supermarkets.MAKRO:
                    price = f'{price[:-2]}.{price[-2:]}'
                
                if promo_element and not(promo_element.text == ''):
                    promo = promo_element.text
                else:
                    promo = None
                
                if image_element and (not self.__image_exists(name)):
                    filename = f'{self.supermarket.RESOURCES_PATH}/{self.supermarket_name.lower()}/product_images/{name}.png'
                    image_element.location_once_scrolled_into_view
                    sleep(1)
                    if not path.isfile(filename):
                        f = open(filename, 'xb')
                        f.close()
                        if not image_element.screenshot(filename):
                            print('Image not saved.')
                    image = filename
                else:
                    image = None
                
                self.products_list.update({name: {"price": price, "promo": promo, "image": image}})
        if (self.supermarket_name == Supermarkets.MAKRO) and (self.last_product):
            self.last_product = products[-1]
        print(f'Done. {prod_count} total products scraped.')

    def __populate_fixtures(self):
        print("Updating database fixtures", end="...")

        # Populate database fixtures.
        output_file = f'{self.supermarket.RESOURCES_PATH}/{self.supermarket_name.lower()}/{self.driver.current_url.replace("/","#")}.json'

        with open(output_file, 'x') as o_file:
            json.dump(self.products_list, o_file, indent=4)
        self.products_list = {}
        print("Done.")

    def __retrieve_urls(self) -> list[str]:
        sup_name = self.supermarket_name.lower()
        urls_file = f'{self.supermarket.RESOURCES_PATH}/{sup_name}/urls.txt'
        with open(urls_file, 'rt', newline='\n') as file:
            urls: list[str] = list()
            for line in file.readlines():
                urls.append(line.removesuffix('\n'))
            return urls
           
    def scrape_products(self):       
        last_page: int = 0
        next_button: WebElement = None
        page_number:int = 0
        if self.supermarket_name == Supermarkets.PNP:
            page_number= int(self.supermarket.get_home_page_url()[self.supermarket.get_home_page_url().index('=')+1:])
        
        existing_fixtures:list[str] = listdir(f'{self.supermarket.RESOURCES_PATH}/{self.supermarket_name.lower()}')
        self.product_images = listdir(f'{self.supermarket.RESOURCES_PATH}/{self.supermarket_name.lower()}/product_images')
        
        print(f"Scraping {self.supermarket_name} products.")
        sleep(1.50)
        
        if ((self.supermarket_name == Supermarkets.WOOLIES) or (self.supermarket_name == Supermarkets.MAKRO)):
            self.urls = self.__retrieve_urls()
            if len(existing_fixtures) > 0:
                for fixture in existing_fixtures:
                    url = fixture.removesuffix('.json').replace('#','/')
                    # Remove existing fixtures.
                    if (url in self.urls):
                        self.urls.remove(url)
                        if self.supermarket_name == Supermarkets.WOOLIES:
                            self.urls.append(f'{url}?No={self.supermarket.PAGE_INCREMENT}&Nrpp=24')
            self.url_count = len(self.urls)
        
        while True:
            page_number += 1
            print(f"\nBrowsing page {page_number}.")

            if self.home_page:
                if (self.supermarket_name == Supermarkets.WOOLIES) or (self.supermarket_name == Supermarkets.MAKRO):
                    # Read urls in ascending order.
                    self.driver.get(self.urls[len(self.urls)-self.url_count])
                    self.url_count -= 1
                    sleep(2.5)
                elif not((self.supermarket_name == Supermarkets.WOOLIES) or (self.supermarket_name == Supermarkets.MAKRO)):
                    self.driver.get(self.supermarket.get_home_page_url())
                    sleep(5)
                    if not((self.supermarket_name == Supermarkets.CHECKERS) or (self.supermarket_name == Supermarkets.SHOPRITE)):
                        try:
                            self.driver.execute_script('arguments[0].click();',
                                                    self.driver.find_element(By.CSS_SELECTOR, self.supermarket.get_page_selectors()['cookie_button']))
                        except NoSuchElementException:
                            pass

                    if (self.supermarket_name == Supermarkets.PNP):
                        last_page = 138
                
                if not((self.supermarket_name == Supermarkets.CHECKERS) or (self.supermarket_name == Supermarkets.SHOPRITE)):
                    # Move the focus to the body segment of the page.
                    self.driver.execute_script("arguments[0].click();",
                                                self.driver.find_element(By.CSS_SELECTOR, self.supermarket.get_page_selectors()['body']))
                    
                # Scroll to the bottom of the page.
                self.__scroll_page(self.supermarket.SCROLL)
                self.home_page = False
            elif not self.home_page:
                selector:str = self.supermarket.get_page_selectors()['next_button']
                if self.supermarket_name == Supermarkets.PNP:
                    if page_number <= last_page:
                        selector = selector.replace('number', f'{page_number}')
                    elif page_number > last_page:
                        break

                try:                            
                    # Click to the next page if it's available.
                    next_button = self.driver.find_element(by=By.CSS_SELECTOR, value=selector)                
                except NoSuchElementException:
                    pass

                try:
                    # In the case where there are still products to be scraped, load the next page.
                    if next_button.is_enabled():
                        self.driver.execute_script("arguments[0].click();", next_button)
                        if (self.supermarket_name == Supermarkets.PNP) or (self.supermarket_name == Supermarkets.MAKRO):
                            self.driver.execute_script("arguments[0].click();",
                                            self.driver.find_element(By.CSS_SELECTOR, self.supermarket.get_page_selectors()['body']))
                            self.__scroll_page(self.supermarket.SCROLL)
                    # Otherwise, if the final page of the products is reached, proceed to the next supermarket website.
                    # Or continue to the next subcategory in the case of Makro.
                    elif not next_button.is_enabled():
                        if self.url_count == 0:
                            print(f'Available items completely scraped for {self.supermarket_name} website.')
                            break
                        # Proceed to the next category if the items are completely scraped for the current category.
                        elif self.supermarket_name == Supermarkets.WOOLIES:
                            self.home_page = True
                            page_number = 0
                except StaleElementReferenceException:
                    self.home_page = True
                    page_number = 0

            sleep(2)

            # Update products list.
            if not(self.supermarket_name == Supermarkets.MAKRO) or ((self.supermarket_name == Supermarkets.MAKRO) and (not self.home_page)):
                self.__update_products_list()

            # Update database fixtures.
            if not(self.supermarket_name == Supermarkets.MAKRO) or ((self.supermarket_name == Supermarkets.MAKRO) and self.home_page):
                self.__populate_fixtures()
                if self.supermarket_name == Supermarkets.MAKRO:
                    response = input('Proceed to the next subcategory?')
                    if response != 'y':
                        exit('Scraping terminated.')
                        
    def __scroll_page(self, amount):
        i = 0
        while i < amount:
            sleep(5)
            self.driver.execute_script("window.scrollBy(0,1000);")
            i += 1

    def __image_exists(self, filename:str) -> bool:
        return f'{filename}.png' in self.product_images