"""A child class of the Supermarket base class."""

from .base_api import Supermarket

class Makro(Supermarket):
	"""The Makro supermarket class implementation."""

	def __init__(self):
		self.__home_page = 'https://www.makro.co.za'
		self.__category_page = f'{self.__home_page}/food/category/sub/c/idcode'
		self.__name = 'makro'
		self.__page_selectors = {
			'product_list': 'div[data-testid="plp_flat_list"] > div > div.css-1dbjc4n',
			'product_id': '',
			'product_name': 'div > div > div:nth-child(2) > div:last-child > div > div > div:last-child > div:last-child > div:last-child > div > a > div[dir="auto"]',
			'product_price': 'div > div > div:nth-child(2) > div:last-child > div > div > div[style="display: flex;"] > div[dir="auto"]',
			'product_promo': 'div.css-1dbjc4n > div > div[dir="auto"]',
			'footer':'',
			# FIXME: next button.
			'next_button': '#react-app > div > div > div > div.css-1dbjc4n.r-13awgt0 > div > div > div.css-1dbjc4n.r-13awgt0 > div > div.css-1dbjc4n.r-1p0dtai.r-1d2f490.r-12vffkv.r-u8s1d.r-zchlnj.r-ipm5af > div.css-1dbjc4n.r-13awgt0.r-12vffkv > div > div > div > div.css-1dbjc4n.r-13awgt0 > div.css-1dbjc4n.r-150rngu.r-eqz5dr.r-16y2uox.r-1wbh5a2.r-11yh6sk.r-1rnoaur.r-1sncvnh > div > div > div > div > div > div > div.css-1dbjc4n.r-14lw9ot.r-1jgb5lz.r-3w0k23.r-1atloto.r-13qz1uu > div.css-1dbjc4n.r-14lw9ot.r-18u37iz.r-13qz1uu > div.css-1dbjc4n.r-13awgt0 > div > div.css-1dbjc4n.r-1awozwy.r-1777fci > div > div > div.css-901oao.r-cqee49.r-ukjfwf.r-1b43r93.r-rjixqe'#'div[class="css-1dbjc4n r-1awozwy r-1777fci"] > div[data-testid="button-LoadMore"]'
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