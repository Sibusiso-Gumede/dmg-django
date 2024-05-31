"""A child class of the Supermarket base class."""

from .base_api import BaseSupermarket

class PicknPay(BaseSupermarket):
	"""The PicknPay supermarket class implementation."""

	def __init__(self):
		super().__init__()
		self.identifier = 30
		self.__query_page = 'https://www.pnp.co.za/search/item'
		self.__home_page = 'https://www.pnp.co.za/c/pnpbase'
		self.__name = 'PicknPay'
		self.__page_selectors = {
			'product_list': 'div.cx-product-container > div > ui-product-grid-item[class="ng-star-inserted"]',
			'product_name': 'div:only-child > div.product-grid-item__info-container > a > span',
			'product_name_alternative': 'div:only-child',
			'product_price': 'div.product-grid-item__info-container > div.product-grid-item__price-container',
			'product_promo': 'div.product-grid-item__info-container > div.product-grid-item__promotion-container',
			'next_button': 'cx-pagination[queryparam="currentPage"] > a[aria-label="page number"]',
			'last_page_button': 'cx-pagination[queryparam="currentPage"] > a:nth-child(5)',
			'browse_nav': 'cx-page-slot[position="NavigationBar"] > cms-category-navigation[class="ng-star-inserted"] > cms-navigation-ui > nav > div:nth-child(2) > ul > li > button',
			'view_all': 'cx-page-slot[position="NavigationBar"] > cms-category-navigation[class="ng-star-inserted"] > cms-navigation-ui > nav > div:nth-child(2) > ul > li > div > ul > li:nth-child(1) > a[class^="list"] > span[class^="action"]',
			'footer': 'body > pnp-root.sparta > div.main-wrapper > ui-storefront > footer.mouse-focus',
			'header': 'body > pnp-root.sparta > div.main-wrapper > ui-storefront > header.mouse-focus'
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