"""A child class of the Supermarket base class."""

from .base_api import BaseSupermarket

class Makro(BaseSupermarket):
	"""The Makro supermarket class implementation."""

	def __init__(self):
		super().__init__()
		self.identifier = 20
		self.__home_page = 'https://www.makro.co.za'
		self.__category_page = f'{self.__home_page}/food/category/sub/c/idcode'
		self.__name = 'Makro'
		self.__page_selectors = {
			'product_list': 'div[data-testid="plp_flat_list"] > div > div.css-1dbjc4n',
			'product_id': '',
			'product_name': 'div > div > div:nth-child(2) > div:last-child > div > div > div:last-child > div:last-child > div:last-child > div > a > div[dir="auto"]',
			'product_price': 'div > div > div:nth-child(2) > div:last-child > div > div > div[style="display: flex;"] > div[dir="auto"]',
			'product_promo': 'div.css-1dbjc4n > div.css-1dbjc4n > div > div[dir="auto"]',
			'product_image': 'div[data-testid="network_image"] > img',
			'body': 'div[style^="min-height"] > div[data-testid="plpScreen"]',
			'next_button': 'div[data-testid="plpScreen"] > div > div > div > div[class="css-1dbjc4n r-14lw9ot r-1jgb5lz r-3w0k23 r-1atloto r-13qz1uu"] > div:nth-child(2) > div:nth-child(2) > div > div[class="css-1dbjc4n r-1awozwy r-1777fci"] > div[data-testid="button-LoadMore"]'
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

	def get_category_page_url(self) -> str:
		return self.__category_page