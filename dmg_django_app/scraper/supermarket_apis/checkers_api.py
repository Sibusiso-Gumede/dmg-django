"""A child class of the Supermarket base class."""

from .generic_api import Supermarket

class Checkers(Supermarket):
	"""The Checkers supermarket class implementation."""

	def __init__(self):
		self.base_address = 'https://www.checkers.co.za'
		self.name = 'checkers'
		self.page_selectors = {
			'product_list': '',
			'product_id': '',
			'product_title': '',
			'product_price': '',
			'product_promo': '',
			'product_img': '',
		}		
		self.page_increment = 1

	def get_supermarket_name(self) -> str:
		"""Returns the name of the supermarket object."""
		return self.name
	
	def products_page_url(self, page_number=0) -> str:
		"""Returns the absolute url of a webpage."""
		return self.base_address
	
	def get_page_increment(self) -> int:
		"""Returns the page increment of the website."""
		return self.page_increment
	
	def get_page_selectors(self) -> dict[str]:
		"""Returns a dictionary of CSS selectors."""
		return self.page_selectors
