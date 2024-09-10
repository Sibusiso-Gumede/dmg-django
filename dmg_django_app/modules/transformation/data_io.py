# Transformation and loading module for managing data.

import json
from io import BytesIO
from PIL import Image, UnidentifiedImageError
from os import path, listdir
from ..supermarket_apis import BaseSupermarket
from .receipt_renderer import ReceiptRenderer, base64

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

def store_image(img: bytes, image_path: str) -> bool:
    '''Stores byte content in image format(png, jpeg, etc).'''
    
    try:
        image = Image.open(BytesIO(img))
    except UnidentifiedImageError or FileNotFoundError:
        print("Image not found or is invalid.")
    else:
        with open(image_path, "xb") as file:
            image.save(file) 

    return path.isfile(image_path)

def retrieve_image(images_dir: str) -> list[Image.Image] | Image.Image:
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

def store_supermarket_records(supermarket: BaseSupermarket) -> None:
    from ...models import Supermarket as SupermarketModel, Product
    
    print("Storing products in database.")
    _name = supermarket.get_supermarket_name().lower()
    products: dict = {}
    for file_name in listdir(f'{supermarket.RESOURCES_PATH}/{_name}/'):
        if('http' in file_name):
            _file = open(f'{supermarket.RESOURCES_PATH}/{_name}/{file_name}', 'r')
            products.update(dict(json.load(_file)))
            _file.close()
    print("\nStoring supermarket record...", end="")
    supermarket_record = SupermarketModel(id=supermarket.identifier,
                                        name=_name.capitalize(),
                                        num_of_products=len(products))
    supermarket_record.save()
    print("Done.")

    print("Storing product records...", end="")
    supermarket_record = SupermarketModel.objects.get(name=_name.capitalize())
    count:int = 0
    for name, details in products.items():
        count += 1
        if (_name == "picknpay") and (details['discounted_price'] is not None):
            _discounted = details['discounted_price']        
        else:
            _discounted = 'R0.00'

        if details['promo'] is None:
            _promo = None
        else:
            _promo = details['promo']
            
        product_record = Product(id=f'{supermarket_record.id}{count}',
                                name=name, price=details['price'], promotion=_promo,
                                supermarket=supermarket_record, discounted_price=_discounted,
                                img_path=details['image'])
        product_record.save()
    print("Done.")
    print("Storage of records completed.")

def separate_prices(price: str) -> list[str]:
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
        if not (x in [' ', '/', 'k', 'g', 'P', 'p', 'e', 'r']):
            _price += x      
            previous = x
    prices.append(_price)       
    return prices

def organize_prices(_list:list[str]) -> dict[str]:
    if float(_list[0].removeprefix('R')) < float(_list[1].removeprefix('R')):
        return {"discounted":_list[0], "price": _list[1]}
    else:
        return {"discounted":_list[1], "price": _list[0]}

def clean_data(s: BaseSupermarket) -> None:
    _name = s.get_supermarket_name().lower()
    for _file in listdir(f'{s.RESOURCES_PATH}/{_name}/'):
        buffer: dict = {}
        if 'http' in _file:
            file = open(f'{s.RESOURCES_PATH}/{_name}/{_file}', "r")
            prods = dict(json.load(file))
            file.close()
            file = open(f'{s.RESOURCES_PATH}/{_name}/{_file}', 'w')
            for name, data in prods.items():
                if s.get_supermarket_name() == 'PicknPay':
                    # if there's more than one price in the same field,
                    # move the lesser price to the discounted_price field.
                    if data.get('price').count('R') > 1:
                        sorted:dict[str] = organize_prices(separate_prices(data.get('price')))
                        buffer.update({name: {"price": sorted.get('price'),
                                            "discounted_price": sorted.get('discounted'),
                                            "promo": data.get('promo'), "image": data.get('image')}})
                    else:
                        buffer.update({data.get('name'): {"price": data.get('price'),
                                                "discounted_price": None,
                                                "promo": data.get('promo'), "image": data.get('image')}})
                elif s.get_supermarket_name() == 'Makro':
                    promo = ''
                    if data.get('promo')[2:].isdigit() or (data.ger('promo') == ''):
                        promo = None
                    buffer.update({name: {'price': data.get('price'), 'promo': promo,
                                    'image': f'{s.RESOURCES_PATH}/{_name}/product_images/{name}.png'}})
            json.dump(buffer, file)
            file.close()

def query_items(query: str, supermarket_name: str = None) -> dict[str]:
    from ...models import Supermarket as SupermarketModel, Product
    
    products = Product.objects
    supermarket = SupermarketModel.objects

    if supermarket_name:
        supermarket = supermarket.get(name__icontains=supermarket_name)   
        products = products.filter(supermarket_id=supermarket.id)
    products = products.filter(name__icontains=query)        
    
    if products: 
        buffer: dict[str] = {}
        # product autosuggestion.
        if supermarket_name:
            for p in products:
                if (not (p.discounted_price == 'R0.00')) and check_for_bargain(p.promotion):
                    buffer.update({p.name: {'price': p.discounted_price, 'promo': p.promotion}})
                else:
                    buffer.update({p.name: {'price': p.price, 'promo': None}})
        # discounted products.
        else:
            for s in supermarket.all():
                buffer2: dict[str] = {}
                for p in products:
                    if s.id == p.supermarket_id:
                        image = base64.b64encode(Image.open(p.image).tobytes()).decode('ascii')
                        if (not (p.discounted_price == 'R0.00')) and check_for_bargain(p.promotion):
                            buffer2.update({p.name: {'price': p.discounted_price, 'image': image, 'promo': p.promotion}})
                        else:
                            buffer2.update({p.name: {'price': p.price, 'image': image, 'promo': None}})
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

def from_base64String_to_png(filename: str, resources_dir: str) -> None:
    with open(filename, '+r') as file:
        products = dict(json.load(file))
        file_buffer: dict = {}
        for name, data in products.items():
            Image.open(BytesIO(base64.b64decode(data.get('image')))).save(f'{resources_dir}/product_images/{name}', 'png')
            file_buffer.update({name: {
                'price': data.get('price'), 'discounted_price': data.get('discounted_price'),
                'promo': data.get('promo'), 'image': f'{resources_dir}/product_images/{name}.png'
            }})
        json.dump(file_buffer, file)

def check_for_bargain(promotion: str) -> bool:
    bargain_substrings = ['FOR', 'Buy', 'for', 'Any', 'any']
    for sub in bargain_substrings:
        if sub in promotion:
            return True
    return False