"""A child class of the Supermarket base class."""

from .generic_api import Supermarket, BeautifulSoup
from transformation import store_content, listdir,  makedirs, retrieve_webpage, path
from time import sleep
from random import choice
import requests
import os
import glob
import json

class Woolworths(Supermarket):
    """The Woolworths supermarket class implementation."""
    
    def __init__(self):
        self.__home_page = 'https://www.woolworths.co.za'
        self.__name = 'woolworths'
        self.__page_selectors = {
			'product_list': '',
			'product_id': '',
			'product_title': '',
			'product_price': '',
			'product_promo': '',
			'product_img': '',
			'search_bar':'',
		}		
        self.__product = ''
        self.__resources_path = f"/home/workstation33/Documents/Development Environment/Projects/discount_my_groceries/dmg_django/supermarket_resources/{self.__name}"
        self.__category_pages_path = f"{self.__resources_path}/category_pages"
        self.__product_view_pages_path = f"{self.__resources_path}/product_view_pages"
        self.__product_images_path = f"{self.__resources_path}/product_images/categories"
        self.__current_product_view_page_url = str()
        self.__current_category_id = str()
        self.__current_category_name = str()
        self.__current_category_page_url = str()
        self.__categories = dict()
        self.__products = dict()
        self.__category_number = int(0)
        self.__pdp_urls = list()
        self.__prior_product_items = None
        self.__max_items_per_category = int(0)
        self.__images_pattern = f"{self.__product_images_path}/*/*.bin"
        self.__query_parameters = f'?No=12&Nrpp={self.__max_items_per_category}'
        self.__headers = {
                        #'Accept': '*/*', 'application/json, text/plain',
                        #'Accept-Encoding': 'gzip, deflate, br',
                        #'Accept-Language': 'en-US,en;q=0.9',
                        #'Content-Length': '3702',
                        #'Content-Type': 'text/plain;charset=UTF-8',
                        #'Sec-Ch-Ua-Platform': '"Linux"',
                        #'Sec-Fetch-Dest': 'document',
                        #'Sec-Fetch-Mode': 'cors',
                        #'Sec-Fetch-Site': 'same-origin',
                        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        }

        with open(f"{self.__resources_path}/categories.json") as file:
            self.__categories = json.load(file)

    def get_page_selectors(self) -> dict[str]:
        return self.__page_selectors
    
    def get_searched_product(self) -> str:
        return self.__product

    def get_supermarket_name(self) -> str:
        """Returns the name of the supermarket object."""
        return self.__name
    
    def store_page_template(self, content) -> None:

        if store_content(content,
                        self.__category_pages_path,
                        self.__current_category_page_url.split('/')[5]):
            print(f"{self.__current_category_name} page stored successfully.")
        else:
            print(f"{self.__current_category_page} not stored successfully.")
    
    def store_product_view_page_template(self) -> None:
        
        self.__current_product_view_page_url = "https://woolworths.co.za/prod/Food/Frozen-Food/Fish-Seafood/Frozen-Mussels-with-Garlic-Herb-Butter-500-g/_/A-6009214621319?isFromPLP=true"
        product_name = self.__current_product_view_page_url.split('/')[7]
        
        if store_content(self.send_request(self.__current_product_view_page_url),
                            self.__product_view_pages_path, product_name):
            print("Page successfully stored.")
        else:
            print("Page not successfully stored.")

    def scrape_items(self):
        print("Scraping of website category pages initiated\n...")
        
        items_range = range(4, 28, 4)
        with requests.Session() as s:   
            s.headers = self.__headers 
            for (category_name, category_details) in zip(self.__categories, self.__categories.values()):
                self.__category_number += 1
                self.__current_category_name = category_name
                self.__current_category_id = category_details['ID']
                self.__max_items_per_category = choice(items_range)
                self.__current_category_page_url = f'{self.__home_page}/cat/Food/{self.__current_category_name}/_/{self.__current_category_id}{self.__query_parameters}'

                if self.__scrape_category(s):
                    print(f"\nScraping of {self.__current_category_name} category products was successfully completed.")
                else:
                    print(f"\nScraping of {self.__current_category_name} category products was partially completed.")
                
                if self.__category_number == 2:
                    breakpoint()

        # Update the product and category files.
        with open(f"{self.__resources_path}/categories.json", "w") as file1, open(f"{self.__resources_path}/products.json", "w") as file2:
            json.dump(self.__categories, file1)
            json.dump(self.__products, file2)

        # Halt a few seconds before sending a request for the pdps.
        sleep(5)

        responses = self.map_function(self.__download_and_store_product_image, self.__pdp_urls)
        for response in responses:
            if not response:
                print(f"\nScraping of product images was partially completed.")        

        print("\nScraping of website category pages terminated.")

    def __download_and_store_product_image(self, pdp: dict):
        # Capture image url from each product's view page.
        pdp = self.parse_response(self.send_request(pdp['url']))
        product_image_url = pdp.find('meta', {'data-react-helmet': 'true', 'property': 'og:image'}).attrs['content']
        sleep(5)
        return store_content(self.send_request(product_image_url), f"{self.__product_images_path}/{pdp['category']}", pdp['url'].split('/')[-3])

    def __delete_product_images(self):
        print("Deleting product images\n...")
        for image in glob.iglob(self.__images_pattern, recursive=True):
            os.remove(image)
        print("\nOperation complete.\n")
    
    def format_promotion_description(self, promo: str):
        """Sorts the product promotion description into a list.
        
           First string is the WRewards promotion and the second
           is the general promotion."""
        
        # Check if the promotion description has the WRewards promotion.
        if 'eward' in promo:
            promotions = list()
            counter = 0

            while True:
                # Make use of ASCII values to distinguish the alphabets in an efficient manner.
                current_letter = ord(promo[counter])
                next_letter = ord(promo[counter+1])
                if (((96 < current_letter) and (current_letter < 123)) or 
                    ((64 < current_letter) and (current_letter < 91))) and (next_letter == 66):
                    # B = 66 'Buy' is on the right. Therefore, append WRewards first to the list.
                    promotions.append(promo[:counter])
                    promotions.append(promo[counter+1:])
                    break
                elif (((96 < current_letter) and (current_letter < 123)) or 
                    ((64 < current_letter) and (current_letter < 91))) and (next_letter == 87):
                    # W = 87 'WRewards' is on the right. Therefore, append WRewards first to the list.
                    promotions.append(promo[counter+1:])
                    promotions.append(promo[:counter])
                    break
                # Return the original text if the discount description only has a WREWARDS deal.
                elif (counter == (len(promo)-1)):
                    promotions.append(promo)
                    break
                counter += 1
            return promotions
        else:
            return promo
        
    def get_category_id(self):
        return self.current_category_id

    def get_category_page_url(self):
        return self.__current_category_page_url
    
    def get_product_images_path(self):
        pass

    def get_product_view_pages_path(self):
        return self.__product_view_pages_path           

    def get_product_image_urls(self):
        pass

    def get_products_page_url(self):
        return self.__current_category_page_url
    
    def get_category_name(self):
        return self.__current_category_name
    
    def get_categories(self):
        return self.__categories
    
    def get_products(self):
        return self.__products
    
    def get_category_page_path(self):
        return self.__category_pages_path
    
    def __scrape_category(self, session, stored=False) -> bool:

        webpage = BeautifulSoup()

        if not stored:
            if self.__category_number > 1:
                #if self.__category_number == choice(range(2, len(self.__categories.keys()+1))):
                #    session.headers['Sec-Fetch-Mode'] = 'navigate'
                #elif session.headers['Sec-Fetch-Mode'] != 'cors':
                #    session.headers['Sec-Fetch-Mode'] = 'cors'
                sleep(5)      
            webpage = self.parse_response(session.get(self.__current_category_page_url).content)
        else:
            webpage = self.parse_response(retrieve_webpage(self.__current_category_name, self.__category_pages_path))        
        
        # Find total items in the category.
        number_of_items = webpage.select_one('#app > div > div > main > div > div:nth-child(3) > div.product-list__list > div > div.list-options')
        print(number_of_items)
        breakpoint()

        images_category_path = f'{self.__product_images_path}/{self.__current_category_name}'
        
        if not path.exists(images_category_path):
            # Create a directory of the current category on the disk if it doesn't exist.    
            makedirs(images_category_path)
        
        #TODO: fix product items issue.    
        product_items = webpage.find_all('div', {'class': 'product-list__item'})
        
        if self.__prior_product_items:
            if product_items[0] == self.__prior_product_items[0]:
                raise FileExistsError
        else:
            self.__prior_product_items = product_items

        self.__products.update({self.__current_category_name: {}})
        total_items = 0
        completed = True
        for product_item in product_items:
            product_name = product_item.find('a', {'class': 'range--title'})
            if product_name:
                product_name = product_name.text
                product_price = product_item.find('strong', {'class': 'price'}).text
                product_promotion = product_item.find('div', {'class': 'product__price-field'}).find_all('a')
                
                if product_promotion:
                    buffer = ""
                    for promotion in product_promotion:
                        buffer += f"{promotion.text}\n"
                    self.__products[self.__current_category_name].update({product_name: 
                                {"product price": product_price, "product promotion": buffer}})                
                else:
                    self.__products[self.__current_category_name].update({product_name: 
                                {"product price": product_price, "product promotion": "None"}})
                            
                pdp_url = product_item.find('a', {'class': 'range--title'}).attrs['href']
                self.__pdp_urls.append({'url': f"{self.__home_page}{pdp_url}",
                                        'category': self.__current_category_name})
                total_items += 1
            else:
                print(f'{self.__current_category_name} product item not scraped.')
                if completed:
                    completed = False

        self.__categories[self.__current_category_name]['Products'] = total_items
        #if self.__category_number == 2:
        #    breakpoint()
        return completed