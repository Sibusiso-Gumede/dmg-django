"""A child class of the Supermarket base class."""

from .base_api import Supermarket

class Checkers(Supermarket):
	"""The Checkers supermarket class implementation."""

	def __init__(self):
		super().__init__()
		self.__home_page = 'https://www.checkers.co.za/search/all?q=item'
		self.__name = 'checkers'
		self.__page_selectors = {
			'product_list': 'div.item-product',
			'product_id': '',
			'product_details': 'div.item-product__details',
			'product_img': '',
			'submit_button':'',
		}
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
