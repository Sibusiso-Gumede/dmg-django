"""A child class of the Supermarket base class."""

from .base_api import Supermarket

class Shoprite(Supermarket):
	"""The Shoprite supermarket class implementation."""

	def __init__(self):
		super().__init__()
		self.__home_page = 'https://www.shoprite.co.za/search/all?q=item'
		self.__name = 'shoprite'
		self.__page_selectors = {
			'product_list': 'div.item-product',
			'product_details': 'div.item-product__details',
		}
		self.detailed_form = True	
		self.text_prod_details = True	

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
