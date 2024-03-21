"""A child class of the Supermarket base class."""

from .base_api import Supermarket

class Woolworths(Supermarket):
    """The Woolworths supermarket class implementation."""
    
    def __init__(self):
        self.__home_page = 'https://www.woolworths.co.za'
        self.__query_page = 'https://www.woolworths.co.za/cat/Food/name/_/idcode'
        self.__name = 'woolworths'
        self.__page_selectors = {
			'product_list': 'div.product-list__item',
			'product_id': '',
			'product_name': 'div[id^="prod_details"] > div.product-card__details > div > div > a.range--title',
            'product_name_alternative': 'div[id^="prod_details"] > div.product-card__details > div.product--desc > a > h2',
			'product_price': 'strong.price',
			'product_promo': 'div[id^="promotion"] > a > div.product__special',
            'browseNav': '#main-nav > ul > li:nth-child(1) > a > div > span',
            'next_button': '#app > div > div > main > div > div:nth-child(3) > div.product-list__list > div > nav > div.pagination__info > li:nth-child(3) > span[class="icon icon--right-dark"]'
        }

    def get_page_selectors(self) -> dict[str]:
        return self.__page_selectors

    def get_supermarket_name(self) -> str:
        """Returns the name of the supermarket object."""
        return self.__name
    
    def get_home_page_url(self) -> str:
        return self.__home_page
    
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
        
    def get_query_page_url(self) -> str:
        return self.__query_page
