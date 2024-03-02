from abc import ABC, abstractclassmethod
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

class Supermarket(ABC):
    """The base class for all supermarket classes."""

    @abstractclassmethod
    def __init__(self):
        pass

    @abstractclassmethod
    def get_supermarket_name(self):
        pass

    @abstractclassmethod
    def get_home_page_url(self):
        pass

    @abstractclassmethod
    def format_promotion_description(self):
        pass

    @abstractclassmethod
    def get_page_selectors(self) -> dict[str]:
        pass

    def map_function(self, func, container: list):
        with ThreadPoolExecutor() as execute:
            return execute.map(func, container)
        
    def parse_response(self, resp_content: bytes) -> BeautifulSoup:
        """Parses the response into a navigatable tree structure."""
        return BeautifulSoup(resp_content, 'lxml')