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
    def __init__(self) -> None:
        self.chromeOptions = webdriver.ChromeOptions()
        self.chromeOptions.add_argument('--headless')
        self.chromeOptions.add_argument('--no-sandbox')
        self.chromeOptions.page_load_strategy = 'normal'
        
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=self.chromeOptions)
        self.driver.set_window_size(1351, 598)
        self.driver.maximize_window()
        self.WAITING_TIME_RANGE = range(1, 3)

        self.current_subcategory: str = ""
        self.last_product: WebElement = None
        self.home_page: bool = False
        self.products_list: dict[str] = {}

        self.url_count: int = 0
        self.urls = list[str]
        self.supermarket_name: str = ""

    def _isRelevant(self, item: str, result: str) -> bool:
        for substring in item.split('%20'):
            if (substring[1:] in result) or (result[0] == 'R' and result[-1].isdigit()) or (result[:3] == 'Buy'):
                return True
        return False

    def __update_products_list(self, _super: BaseSupermarket):
        print('\nScraping product list', end="...")
        products = self.driver.find_elements(by=By.CSS_SELECTOR, value=_super.get_page_selectors()['product_list'])
        name: str = ""
        promo: str = ""
        price: str = ""
        image: str = ""
        prod_count: int = 0
        prod_name_exception: bool = False
        name_element: WebElement = None
        price_element: WebElement = None
        promo_element: WebElement = None
        image_element: WebElement = None

        if (self.supermarket_name == Supermarkets.MAKRO) and (not self.home_page) and self.last_product:
            products = products[products.index(self.last_product)+1:]

        for product in products:
            prod_count += 1
            try:    
                name_element = product.find_element(by=By.CSS_SELECTOR, value=_super.get_page_selectors()['product_name'])
                price_element = product.find_element(by=By.CSS_SELECTOR, value=_super.get_page_selectors()['product_price'])
                promo_element = product.find_element(by=By.CSS_SELECTOR, value=_super.get_page_selectors()['product_promo'])
                image_element = product.find_element(by=By.CSS_SELECTOR, value=_super.get_page_selectors()['product_image'])
            except NoSuchElementException as error:
                line = traceback.format_exception_only(error)[0]
                if _super.get_page_selectors()['product_name'] in line:
                    name_element = product.find_element(by=By.CSS_SELECTOR, value=_super.get_page_selectors()['product_name_alternative'])
                    prod_name_exception = True
                elif _super.get_page_selectors()['product_price'] in line:
                    price_element = None
                elif _super.get_page_selectors()['product_promo'] in line:
                    promo_element = None
                elif _super.get_page_selectors()['product_image'] in line:
                    image_element = None
                    print("\nProduct image not visible.")
            finally:
                if (self.supermarket_name == Supermarkets.PNP) and (prod_name_exception):
                    name = name_element.get_dom_attribute("data-cnstrc-item-name")
                else:
                    name = name_element.text
                
                price = price_element.text
                if self.supermarket_name == Supermarkets.MAKRO:
                    price = f'{price[:-2]}.{price[-2:]}'
                
                if promo_element:
                    promo = promo_element.text
                else:
                    promo = "NULL"
                
                if image_element:
                    image_element.location_once_scrolled_into_view
                    print(f'\nScreenshoting product {prod_count}.')
                    sleep(1)
                    filename = f'{_super.RESOURCES_PATH}/{self.supermarket_name.lower()}/product_images/{name}.png'
                    if not path.isfile(filename):
                        f = open(filename, 'xb')
                        f.close()
                        if not image_element.screenshot(filename):
                            exit('Image not saved.') # system exit.
                    image = filename
                else:
                    image = ''
                
                self.products_list.update({name: {"price": price, "promo": promo, "image": image}})
        if (self.supermarket_name == Supermarkets.MAKRO) and (self.last_product):
            self.last_product = products[-1]
        print("Done.")

    def __populate_fixtures(self, _supermarket: BaseSupermarket):
        print("Updating database fixtures", end="...")

        # Populate database fixtures.
        output_file = f'{_supermarket.RESOURCES_PATH}/{self.supermarket_name.lower()}/{self.driver.current_url.replace("/","#")}.json'

        with open(output_file, 'x') as o_file:
            json.dump(self.products_list, o_file, indent=4)
        self.products_list = {}
        print("Done.")

    def __retrieve_urls(self, _supermarket: BaseSupermarket) -> list[str]:
        sup_name = self.supermarket_name.lower()
        urls_file = f'{_supermarket.RESOURCES_PATH}/{sup_name}/{sup_name}_urls.txt'
        with open(urls_file, 'rt', newline='\n') as file:
            urls: list[str] = list()
            for line in file.readlines():
                urls.append(line.removesuffix('\n'))
            return urls
           
    def scrape_products(self, supermarket: BaseSupermarket):
        divisor_range: list[int] = range(2, 6)       
        last_page: int = 0
        next_button: WebElement = None
        self.home_page = True
        page_number:int = 0
        self.supermarket_name = supermarket.get_supermarket_name()
        existing_fixtures:list[str] = listdir(f'{supermarket.RESOURCES_PATH}/{self.supermarket_name.lower()}')
        
        print(f"Scraping {self.supermarket_name} products.")
        sleep(1.50)
        
        if ((self.supermarket_name == Supermarkets.WOOLIES) or (self.supermarket_name == Supermarkets.MAKRO)):
            self.urls = self.__retrieve_urls(supermarket)
            if len(existing_fixtures) > 0:
                for fixture in existing_fixtures:
                    try:
                        # Remove existing fixtures.
                        self.urls.remove(fixture.removesuffix('.json').replace('#','/'))
                    except ValueError:
                        # If the fixture is not found, continue.
                        pass
            self.url_count = len(self.urls)
        
        while True:
            page_number += 1
            print(f"\nBrowsing page {page_number}.")

            if self.home_page:
                if (self.supermarket_name == Supermarkets.WOOLIES) or (self.supermarket_name == Supermarkets.MAKRO):
                    # Read urls in ascending order.
                    self.driver.get(self.urls[self.url_count-1])
                    self.url_count -= 1
                    sleep(5)
                elif not (self.supermarket_name == Supermarkets.WOOLIES):
                    if not (self.supermarket_name == Supermarkets.MAKRO):
                        self.driver.get(supermarket.get_home_page_url())
                        sleep(5)
                        if (self.supermarket_name == Supermarkets.PNP) or (self.supermarket_name == Supermarkets.MAKRO):
                            try:
                                self.driver.execute_script('arguments[0].click();',
                                                       self.driver.find_element(By.CSS_SELECTOR, supermarket.get_page_selectors()['cookie_button']))
                            except NoSuchElementException:
                                pass
                    if not ((self.supermarket_name == Supermarkets.PNP) or (self.supermarket_name == Supermarkets.MAKRO)):
                        self.driver.find_element(by=By.CSS_SELECTOR, value=supermarket.get_page_selectors()['browse_nav']).click()
                    elif (self.supermarket_name == Supermarkets.PNP) or (self.supermarket_name == Supermarkets.MAKRO):
                        # Move the focus to the body segment of the page.
                        self.driver.execute_script("arguments[0].click();",
                                                    self.driver.find_element(By.CSS_SELECTOR, supermarket.get_page_selectors()['body']))
                        
                        # Scroll to the bottom of the page.
                        i = 0
                        while i < 10:
                            sleep(5)
                            self.driver.execute_script("window.scrollBy(0,1000);")
                            i += 1

                        if self.supermarket_name == Supermarkets.PNP:
                            href: str = self.driver.find_element(By.CSS_SELECTOR, supermarket.get_page_selectors()['last_page_button']).get_dom_attribute('href')
                            last_page = int((href[href.find('='):])[1:])
                self.home_page = False
            elif not self.home_page:
                selector:str = supermarket.get_page_selectors()['next_button']
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
                            self.actions.scroll_by_amount(0, 550)
                            sleep(5)
                            for y in range(0, 8):
                                self.actions.perform()
                            sleep(5)
                            self.actions.reset_actions()                        
                    # Otherwise, if the final page of the products is reached, proceed to the next supermarket website.
                    # Or continue to the next subcategory in the case of Makro.
                    elif not next_button.is_enabled():
                        if self.url_count == 0:
                            print(f'Available items completely scraped for {self.supermarket_name} website.')
                            break
                        # Proceed to the next category if the items are completely scraped for the current category.
                        elif self.supermarket_name == Supermarkets.WOOLIES:
                            self.home_page = True
                except StaleElementReferenceException:
                    self.home_page = True

            sleep((choice(self.WAITING_TIME_RANGE))/(choice(divisor_range)))

            # Update products list.
            if not(self.supermarket_name == Supermarkets.MAKRO) or ((self.supermarket_name == Supermarkets.MAKRO) and (not self.home_page)):
                self.__update_products_list(supermarket)

            # Update database fixtures.
            if not(self.supermarket_name == Supermarkets.MAKRO) or ((self.supermarket_name == Supermarkets.MAKRO) and self.home_page):
                self.__populate_fixtures(supermarket)
