"""A child class of the Supermarket base class."""

from .generic_api import Supermarket, BeautifulSoup

class Spar(Supermarket):
	"""The Spar supermarket class implementation."""

	def __init__(self):
		self.base_address = 'https://www.spar.co.za'
		self.name = 'spar'	
		self.page_increment = 1
		self.product_image_urls = list[str]

	def get_supermarket_name(self) -> str:
		"""Returns the name of the supermarket object."""
		return self.name
	
	def products_page_url(self, page_number=0) -> str:
		"""Returns the absolute url of a webpage."""
		return f'{self.base_address}/Specials'
	
	def get_page_increment(self) -> int:
		"""Returns the page increment of the website."""
		return self.page_increment
	
	def get_product_image_urls(self) -> list:
		"""Returns a list of product image urls."""
		return self.product_image_urls
	
	def set_supermarket_attributes(self, page: BeautifulSoup):
		"""Initializes the supermarket object attributes."""
		products = page.find('ul', {'class': 'slides', 'id': 'slideContainer'}).find_all('li')
		for product in products:
			image_url = product.find('div', {'class': 'item-image'})
			if image_url != None:
				url = str(self.base_address+image_url.find('img').attrs['src']).replace('=280', '=1120')
				self.product_image_urls.append(url)

	def format_promo_description(self) -> str or None:
		"""Returns a formatted promotion description of a product."""
		return None

	def get_images_path(self):
		return f"/home/workstation33/Documents/Development Environment/Projects/discount_my_groceries/dmg_django/supermarket_resources/{self.name}/Product Images"