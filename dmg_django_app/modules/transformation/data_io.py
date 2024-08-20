# Transformation and loading module for managing data.

import json
from io import BytesIO
from PIL import Image, UnidentifiedImageError
from os import path, listdir, makedirs
from ..supermarket_apis import BaseSupermarket, Makro
from ..common import Supermarkets, ASSETS_DIR
from .receipt_renderer import ReceiptRenderer, base64
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
        if (supermarket_name == "picknpay") and (data['discounted_price'] is not None):
            _discounted = data['discounted_price']        
        else:
            _discounted = 'R0.00'

        if data['promo'] is None:
            _promo = "NULL"
        else:
            _promo = data['promo']
            
        product_record = Product(id=f'{supermarket_record.id}{count}',
                                name=name, price=data['price'], promotion=_promo,
                                supermarket=supermarket_record, discounted_price=_discounted)
                                #image=BytesIO((base64.b64decode(data['image']))))
        product_record.save()

def store_supermarket_records() -> None:
    print("Storage of records initiated...")
    _choice = input("\nStore supermarket records...Y/N\n>>>")
    for name, supermarket in Supermarkets.SUPERMARKETS.items():
        name = name.lower()
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

def query_items(query: str, supermarket_name: str = None) -> dict[str]:
    products = Product.objects
    supermarket = SupermarketModel.objects

    if supermarket_name:
        supermarket = supermarket.get(name__icontains=supermarket_name)   
        products = products.filter(supermarket_id=supermarket.id)
    products = products.filter(name__icontains=query)        
    
    if products: 
        buffer: dict[str] = {}
        if supermarket_name:
            for p in products:
                if not (p.discounted_price == 'R0.00'):
                    buffer.update({p.name: p.discounted_price})
                else:
                    buffer.update({p.name: p.price})
        else:
            for s in supermarket.all():
                buffer2: dict[str] = {}
                for p in products:
                    if s.id == p.supermarket_id:
                        if not (p.discounted_price == 'R0.00'):
                            buffer2.update({p.name: p.discounted_price})
                        else:
                            buffer2.update({p.name: p.price})
                if buffer2:
                    buffer.update({s.name: buffer2})
        return buffer        
    else:
        return dict()
    
def receipt(data: dict[str]) -> dict[str]:
    receiptifier = ReceiptRenderer(data)
    return receiptifier.render()

def string_ascii_total(string:str) -> str:
    accumulator:int = 0
    ascii_totals:list[int] = []
    for term in string.split(" "):
        for character in term:
            accumulator += ord(character)
        ascii_totals.append(accumulator)
        accumulator = 0

def scrape_products():
    from ..extraction import Scraper
    s = Scraper()
    m = Makro()
    s.scrape_products([m])