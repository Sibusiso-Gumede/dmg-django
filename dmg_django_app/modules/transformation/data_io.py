# Transformation and loading module for managing data.

import json
from io import BytesIO
from pathlib import Path
from PIL import Image, UnidentifiedImageError
from django.db import connection
from django.core.files import File
from os import path, listdir, makedirs
from ..supermarket_apis import BaseSupermarket
from ..common import Supermarkets
from ...models import Supermarket as SupermarketModel, Product

TITLE_LENGTH: int = 30

def store_content(content: bytes, path_: str, content_name: str) -> bool:
    """Stores the content of the response in bytes.
        Returns a true/false to confirm if the content
        is successfully stored."""

    write_bytes = BytesIO(content)
    path_ += f"/{content_name}.bin"
    
    try:
        with open(path_, "xb") as file:
            file.write(write_bytes.getbuffer())
    except FileExistsError:
        pass

    return path.isfile(path_)

def retrieve_webpage(content_name: str, path_: str) -> bytes:
    """Retrieves the stored contents of a page."""
    
    payload = bytes()
    with open(path_+f"/{content_name}.bin", "rb") as file:
        
        # Read a maximum of 8kilobytes data per cycle
        # and append it to the payload.
        
        buffer_size = 2**10*8 
        buffer = file.read(buffer_size)
        while buffer:
            payload += buffer
            buffer = file.read(buffer_size)

    return payload

def store_image(img: bytes, path_: str, img_name: str) -> bool:
    '''Stores byte content in image format(png, jpeg, etc).'''
    
    absolute_path = f"{path_}/{img_name}.png"
    if not path.exists(path_):
        makedirs(path_)
    try:
        image = Image.open(BytesIO(img))
    except UnidentifiedImageError or FileNotFoundError:
        print("Image not found or is invalid.")
    else:
        with open(absolute_path, "xb") as file:
            image.save(file, "png") 

    return path.isfile(absolute_path)

def retrieve_image(images_dir: str):
    '''Retrieves an image file stored on disk and
        returns it in Image format.'''
    
    files = listdir(images_dir)

    if files:
        # when there's more than one file in the directory
        # return a list of image file names, else return one image file
        # name.
        if len(files) > 1:
            images = list()
            for file in files:
                file = f"{images_dir}/{file}"
                images.append(Image.open(file))
            return images
        else:
            files[0] = f"{images_dir}/{files[0]}"
            return Image.open(files[0])
    elif files is None:
        raise FileNotFoundError

def resize_image(image: Image):
    '''Resizes an image.'''
    width, height = image.size
    return image.crop((width/2, 0.5, width, height))     

def store_supermarket_record(s:BaseSupermarket, nr_of_prods:int) -> None:
    print("\nStoring supermarket records...")
    supermarket_record = SupermarketModel(id=s.identifier,
                                        name=s.get_supermarket_name(),
                                        num_of_products=nr_of_prods)
    supermarket_record.save()

def store_product_records(supermarket_name: str, products: dict[str]) -> None:
    print("\nStoring product records...")
    supermarket_record = SupermarketModel.objects.get(name=supermarket_name)
    count:int = 0
    for name, data in products.items():
        count += 1
        product_record = Product(id=f'{supermarket_record.id}{count}',
                                name=name, price=data['price'], promotion=data['promo'],
                                supermarket=supermarket_record, discounted_price=data['discounted_price'])
        product_record.save()

def createProductsFixtures() -> None:
    for name, supermarket in Supermarkets.SUPERMARKETS.items():
        file = open(f'{supermarket.RESOURCES_PATH}/{name}/{name}_products.json', 'r')
        products = store_supermarket_record(supermarket, file)
        fixture:dict[str] = {}
        for name, data in products.items():
            fixture.update({"model": "dmg_django_app.product",
                            "fields": {
                                "id":"", 
                            }})
            # TODO: ...

def store_supermarket_records() -> None:
    print("Storage of records initiated...")
    _choice = input("\nStore supermarket records...Y/N\n>>>")
    for name, supermarket in Supermarkets.SUPERMARKETS.items():
        _file = open(f'{supermarket.RESOURCES_PATH}/{name}/{name}_products.json','r')
        _products: dict[str] = dict(json.load(_file))                
        if _choice == 'Y':    
            store_supermarket_record(supermarket, len(list(_products.keys())))   
        store_product_records(name, _products)
        _file.close()
    print("\nStorage of records completed.")

def seperate_prices(price: str) -> list[str]:
    '''Extracts a list of prices contained within a single string
        and returns a list of the seperated prices.
        e.g. "R99.99 R89.99" -> ["R99.99", "R89.99"]'''
    prices:list[str] = []
    _price:str = ''
    previous:str = '' 
    for x in price:
        if (x == 'R') and (previous.isdigit() or (previous == ' ')):
            prices.append(_price)
            _price = ''
        if not ((x == ' ') or (x == '/') or (x == 'k') or (x == 'g')):
            _price += x      
            previous = x
    prices.append(_price)       
    return prices

def organize_prices(_list:list[str]) -> dict[str]:
    if float(_list[0].removeprefix('R')) < float(_list[1].removeprefix('R')):
        return {"discounted":_list[0], "price": _list[1]}
    else:
        return {"discounted":_list[1], "price": _list[0]}

def clean_data(s: BaseSupermarket) -> dict[str]:
    with open(f'{s.RESOURCES_PATH}/{s.get_supermarket_name()}/{s.get_supermarket_name()}_products.json', "+r") as file:
        prods = dict(json.load(file))
        buffer: dict = {}
        for name, data in prods.items():
            # if there's more than one price in the same field,
            # move the lesser price to the discounted_price field.
            if data.get('price').count('R') > 1:
                sorted:dict[str] = organize_prices(seperate_prices(data.get('price')))
                buffer.update({name: {"price": sorted.get('price'),
                                        "discounted_price": sorted.get('discounted'),
                                        "promo": data.get('promo')}})
            else:
                buffer.update({name: {"price": data.get('price'),
                                        "discounted_price": None,
                                        "promo": data.get('promo')}})
        json.dump(buffer, file)
        return buffer
    
def shorten_string(s:str) -> str:
    ''' Returns a string alias of the complete string.
        includes the first two words and the last.
    '''
    formatted: str = ""
    count: int = 0
    # find the position of the first digit in the string.
    while count < len(s):
        if s[count].isdigit():
            break
        count += 1

    # remove the rest of the string starting from the first 
    # digit found.
    formatted = s[:count]

    # slice formatted string if it's longer than 30 characters.
    if len(formatted) > TITLE_LENGTH:
        formatted = formatted[:TITLE_LENGTH-1]

    restricted:set[str] = ["with", "in", "on", "No", "&"]
    formatted_terms:list[str] = []
    formatted_terms = formatted.split(' ')

    # find the last term of the formatted string.
    # ascertain that it meets the required format constraints.
    # the constraints are: a string should not end with a 
    # prepostion or it's last term should not be partial.
    while True:
        if (formatted_terms[-1] in restricted) or (not (formatted_terms[-1] == s.split(' ')[len(formatted_terms)-1])):
            formatted_terms.pop()
            formatted = ' '.join(formatted_terms)
        else:
            break            
    return formatted

def query_items(query: str, supermarket_name: str = None, receiptify: bool = False) -> dict[str] | None:
    supermarket = None
    products = None
    # In the case where a supermarket name is specified.
    if not (supermarket_name == None):
        supermarket = SupermarketModel.objects.get(name__icontains=supermarket_name)   
        products = Product.objects.filter(supermarket_id=supermarket.id)
        products = products.filter(name__icontains=query)
    elif supermarket_name == None:
        products = Product.objects.filter(name__icontains=query)
        
    if products == None:
        return None
    else:
        buffer: dict[str] = {}
        name: str = ""
        for p in products:
            if receiptify and (not (len(p.name) <= TITLE_LENGTH)):
                name = shorten_string(p.name)
            else:
                name = p.name
            if not (p.discounted_price == 'R0.00'):
                buffer.update({name: {"price": p.discounted_price, "supermarket_name": p.supermarket.name}})
            else:
                buffer.update({name: {"price": p.price, "supermarket_name": p.supermarket.name}})   
        return buffer

def string_ascii_total(string:str) -> str:
    accumulator:int = 0
    ascii_totals:list[int] = []
    for term in string.split(" "):
        for character in term:
            accumulator += ord(character)
        ascii_totals.append(accumulator)
        accumulator = 0