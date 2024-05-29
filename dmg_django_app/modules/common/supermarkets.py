"""The implementation of Supermarkets."""
from ..supermarket_apis import Shoprite, Checkers, PicknPay, Makro, Woolworths

class Supermarkets():
    """Supermarket objects, grouped in a single container - 
    for ease of access and package navigation."""
    
    PNP = 'Picknpay'
    WOOLIES = 'Woolworths'
    SHOPRITE = 'Shoprite'
    CHECKERS = 'Checkers'
    MAKRO = 'Makro'

    SUPERMARKETS: dict = {
        WOOLIES: Woolworths(),
        SHOPRITE: Shoprite(),
        PNP: PicknPay(),
        CHECKERS: Checkers(),
        MAKRO: Makro()
    }