"""A child class of the Supermarket base class."""

from .generic_api import Supermarket, BeautifulSoup

class PicknPay(Supermarket):
	"""The PicknPay supermarket class implementation."""

	def __init__(self):
		super().__init__()
		self.__home_page = 'https://www.pnp.co.za/search/'
		self.__name = 'picknpay'
		self.__page_selectors = {
			'product_list': 'ui-product-grid-item',
			#'div[class^="cx-product-container"] > div[class$="ng-star-inserted"]',
			'product_id': '',
			'product_title': 'div[class^="product-grid-item"]',
			'product_price': '',
			'product_promo': '',
			'product_img': '',
			'attributes': {'name': 'data-cnstrc-item-name',
							'price': 'data-cnstrc-item-price',}
		}		
		self.attributes = True

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