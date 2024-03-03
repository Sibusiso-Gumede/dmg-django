"""A child class of the Supermarket base class."""

from .generic_api import Supermarket

class Shoprite(Supermarket):
	"""The Shoprite supermarket class implementation."""

	def __init__(self):
		self.__base_address = 'https://www.shoprite.co.za'
		self.__name = 'shoprite'
		self.__page_selectors = {
			'product': 'div.item-product',
			'product_id': '',
			'product_name': 'div.item-product__details > h3.item-product__name > a.product-listening-click',
			'product_price': '',
			'product_promo': '',
			'product_img': '',
			'search_bar':'#js-site-search-input',
		}
		self.__page_increment = 1		

	def get_supermarket_name(self) -> str:
		"""Returns the name of the supermarket object."""
		return self.__name
	
	def get_home_page_url(self) -> str:
		"""Returns the absolute url of a webpage."""
		return self.__base_address
	
	def get_page_increment(self) -> int:
		"""Returns the page increment of the website."""
		return self.__page_increment
	
	def get_page_selectors(self) -> dict[str]:
		"""Returns a dictionary of CSS selectors."""
		return self.__page_selectors
	
	def format_promotion_description(self):
		pass
