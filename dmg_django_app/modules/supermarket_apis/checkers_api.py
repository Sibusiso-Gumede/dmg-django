"""A child class of the Supermarket base class."""

from .base_api import BaseSupermarket

class Checkers(BaseSupermarket):
	"""The Checkers supermarket class implementation."""

	SCROLL = 4

	def __init__(self):
		super().__init__()
		self.identifier = 10
		self.__query_page = 'https://www.checkers.co.za'
		self.__home_page = 'https://www.checkers.co.za/c-2256/All-Departments?q=%3Arelevance%3AbrowseAllStoresFacetOff%3AbrowseAllStoresFacetOff&page=53'
		self.__name = 'Checkers'
		self.__page_selectors = {
			'product_list': 'div.item-product',
			'product_name': 'div.item-product__details > h3.item-product__name > a',
			'product_price': 'span.now',
			'product_image': 'figure.item-product__content > div.item-product__image > a > img',
			'body': 'body.page-productGrid',
			'product_promo': 'div.item-product__details > span.item-product__valid',
			'next_button': 'ul[class="pagination pull-right"] > li.pagination-next > a'
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

	def get_query_page_url(self):
		return self.__query_page