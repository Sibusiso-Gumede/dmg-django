from abc import ABC, abstractclassmethod

class Supermarket(ABC):
    """The base class for all supermarket classes."""
    RESOURCES_PATH = '/home/workstation33/Documents/Development Environment/Projects/discount_my_groceries/dmg_django/dmg_django_app/resources'

    @abstractclassmethod
    def __init__(self):
        pass

    @abstractclassmethod
    def get_supermarket_name(self) -> str:
        pass

    @abstractclassmethod
    def get_home_page_url(self) -> str:
        pass

    @abstractclassmethod
    def format_promotion_description(self):
        pass

    @abstractclassmethod
    def get_page_selectors(self) -> dict[str]:
        pass

    @abstractclassmethod
    def get_category_page_url(self) -> str:
        pass