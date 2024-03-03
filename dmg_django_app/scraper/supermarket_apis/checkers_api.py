"""A child class of the Supermarket base class."""

from .generic_api import Supermarket

class Checkers(Supermarket):
	"""The Checkers supermarket class implementation."""

	def __init__(self):
		super().__init__()
		self.__home_page = 'https://www.checkers.co.za'
		self.__name = 'checkers'
		self.__page_selectors = {
			'product_list': '',
			'product_id': '',
			'product_title': '',
			'product_price': '',
			'product_promo': '',
			'product_img': '',
		}
		self.query_parameters = True
		self.parameters = ""

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
