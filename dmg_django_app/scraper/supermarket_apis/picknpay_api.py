"""A child class of the Supermarket base class."""

from .base_api import Supermarket

class PicknPay(Supermarket):
	"""The PicknPay supermarket class implementation."""

	def __init__(self):
		self.__query_page = 'https://www.pnp.co.za/search/item'
		self.__home_page = 'https://www.pnp.co.za'
		self.__name = 'picknpay'
		self.__page_selectors = {
			'product_list': 'ui-product-grid-item',
			'product_name': 'div.product-grid-item__info-container > a > span',
			'product_price': 'div.product-grid-item__info-container > div.product-grid-item__price-container',
			'product_promo': 'div.product-grid-item__info-container > div.product-grid-item__promotion-container',
			'next_button': 'cx-pagination > a[href$="number"]',
			'browse_nav': 'nav.ng-tns-c330-0 > div > ul > li[class^="navigation-item"] > button',
			'view_all': 'nav.ng-tns-c330-0 > div > ul > li[class^="navigation-item"] > div > ul > li > a > span:nth-child(2)'
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

	def get_query_page_url(self) -> str:
		return self.__query_page