"""A child class of the Supermarket base class."""

from .base_api import Supermarket

class Makro(Supermarket):
	"""The Makro supermarket class implementation."""

	def __init__(self):
		self.__home_page = 'https://www.makro.co.za'
		self.__category_page = f'{self.__home_page}/food/category/sub/c/idcode'
		self.__name = 'makro'
		self.__page_selectors = {
			'product_list': 'div[dir="auto"]',
			'product_id': '',
			'product_title': '',
			'product_price': '',
			'product_promo': '',
			'footer':'',
		}		

	def get_supermarket_name(self) -> str:
		"""Returns the name of the supermarket object."""
		return self.__name
	
	def get_home_page_url(self) -> str:
		"""Returns the absolute url of a webpage."""
		return self.__home_page
	
	def get_page_selectors(self) -> dict[str]:
		"""Returns a dictionary of CSS selectors."""
		return self.__page_selectors

	def format_promotion_description(self):
		pass

	def get_category_page_url(self) -> str:
		return self.__category_page