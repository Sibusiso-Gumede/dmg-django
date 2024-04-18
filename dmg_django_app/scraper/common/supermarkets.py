"""The implementation of Supermarkets."""
from ..supermarket_apis import Shoprite, Checkers, PicknPay, Makro, Woolworths

class Supermarkets():
    """Group of supermarket names."""
    
    PNP = 'picknpay'
    WOOLIES = 'woolworths'
    SHOPRITE = 'shoprite'
    CHECKERS = 'checkers'
    MAKRO = 'makro'

    SUPERMARKETS: dict[str] = {
        WOOLIES: Woolworths(),
        SHOPRITE: Shoprite(),
        PNP: PicknPay(),
        CHECKERS: Checkers(),
        MAKRO: Makro()
        }