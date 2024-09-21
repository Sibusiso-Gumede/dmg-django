from abc import ABC
from ....dmg_django.settings import BASE_DIR

class BaseSupermarket(ABC):
    """The base class for all supermarket classes."""
    RESOURCES_PATH = BASE_DIR / 'dmg_django_app/resources'

    @classmethod
    def __init__(self):
        self.products:int = 0
        self.identifier:int = 0

    @classmethod
    def get_supermarket_name(self) -> str:
        pass

    @classmethod
    def get_home_page_url(self) -> str:
        pass

    @classmethod
    def format_promotion_description(self):
        pass

    @classmethod
    def get_page_selectors(self) -> dict[str]:
        pass

    @classmethod
    def get_category_page_url(self) -> str:
        pass

    def increase_product_count(self) -> None:
        self.products += 1