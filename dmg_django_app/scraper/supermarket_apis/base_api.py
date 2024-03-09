from abc import ABC, abstractclassmethod

class Supermarket(ABC):
    """The base class for all supermarket classes."""

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
    def get_query_page_url(self) -> str:
        pass