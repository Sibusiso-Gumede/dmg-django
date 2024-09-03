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
			'product_image': 'a.product-grid-item__image-container > cx-media.product-grid-item__image-container__image > img',
			'next_button': 'cx-pagination[queryparam="currentPage"] > a[aria-label="page number"]',
			'last_page_button': 'body > pnp-root > div > ui-storefront > main > cx-page-layout > cx-page-slot.ProductGridSlot.has-components > cms-product-list > div > section > div > div > div > div.cx-sorting.bottom > div > div > div > cx-pagination > a.end.ng-star-inserted',
			'browse_nav': 'cx-page-slot[position="NavigationBar"] > cms-category-navigation[class="ng-star-inserted"] > cms-navigation-ui > nav > div:nth-child(2) > ul > li > button',
			'view_all': 'cx-page-slot[position="NavigationBar"] > cms-category-navigation[class="ng-star-inserted"] > cms-navigation-ui > nav > div:nth-child(2) > ul > li > div > ul > li:nth-child(1) > a[class^="list"] > span[class^="action"]',
			'body': 'body',
			'footer': 'body > pnp-root.sparta > div.main-wrapper > ui-storefront > footer.mouse-focus',
			'header': 'body > pnp-root.sparta > div.main-wrapper > ui-storefront > header.mouse-focus',
			'cookie_button': 'div.cookie-item > button.accept',
		}
		self.scroll_count:int = 5

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
	
	def get_scroll_count(self) -> int:
		return self.scroll_count