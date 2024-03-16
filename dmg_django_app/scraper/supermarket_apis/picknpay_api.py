"""A child class of the Supermarket base class."""

from .base_api import Supermarket

class PicknPay(Supermarket):
	"""The PicknPay supermarket class implementation."""

	def __init__(self):
		self.__query_page = 'https://www.pnp.co.za/search/item'
		self.__home_page = 'https://www.pnp.co.za/c/pnpbase'
		self.__name = 'picknpay'
		self.__page_selectors = {
			'product_list': 'div.cx-product-container > ui-product-grid-item[class="ng-star-inserted"]',
			'product_name': 'div.product-grid-item__info-container > a > span',
			'product_price': 'div.product-grid-item__info-container > div.product-grid-item__price-container',
			'product_promo': 'div.product-grid-item__info-container > div.product-grid-item__promotion-container',
			'next_button': 'cx-pagination > a[href$="number"]',
			'browse_nav': 'cms-navigation-ui > nav:first-child > div:nth-child(2) > ul > li > button',
			'view_all': 'cms-navigation-ui > nav:first-child > div:nth-child(2) > ul > li > div[class^="navigation-child"] > ul > li > a[class^="list"] > span[class^="action"]',
			'products_found': 'body > pnp-root > div > ui-storefront > main > cx-page-layout > cx-page-slot.ProductGridSlot.has-components.ng-star-inserted > cms-product-list > div > section > div > div > div > div.cx-sorting.top > div > h2 > span',
			#'cx-page-slot[position="ProductGridSlot"] > cms-product-list > section[class^="cx-page-section"] > div > div[class^="row"] > div[class^="col"] > div[class^="cx-sorting"] > div[class^="row"] > h2[class="title-with-quantity"] > span'
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