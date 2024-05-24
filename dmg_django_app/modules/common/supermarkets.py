"""The implementation of Supermarkets."""
from ..supermarket_apis import Shoprite, Checkers, PicknPay, Makro, Woolworths

class Supermarkets():
    """Supermarket objects, grouped in a single container - 
    for ease of access and package navigation."""
    
    PNP = 'picknpay'
    WOOLIES = 'woolworths'
    SHOPRITE = 'shoprite'
    CHECKERS = 'checkers'
    MAKRO = 'makro'

    SUPERMARKETS: dict = {
        WOOLIES: Woolworths(),
        SHOPRITE: Shoprite(),
        PNP: PicknPay(),
        CHECKERS: Checkers(),
        MAKRO: Makro()
    }