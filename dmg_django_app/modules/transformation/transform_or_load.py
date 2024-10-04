# Transformation and loading module for managing data.

import json
from io import BytesIO
from PIL import Image, UnidentifiedImageError
from os import path, listdir, makedirs
from .receipt_renderer import ReceiptRenderer, base64
from ...models import Supermarket as SupermarketModel, Product, Common

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

def store_supermarket_records(supermarkets: list) -> None:
    import shutil
    for supermarket in supermarkets:
        _name = supermarket.get_supermarket_name().lower()
        print(f"Storing {_name.capitalize()} fixtures in database.")
        
        print("Storing supermarket record...", end="")
        supermarket_record = SupermarketModel(id=supermarket.identifier,
                                            name=_name.capitalize(),
                                            num_of_products=len(products))
        supermarket_record.save()
        print("Done.")
        
        products: dict = {}
        for file_name in listdir(f'{supermarket.RESOURCES_PATH}/{_name}/'):
            if('http' in file_name):
                _file = open(f'{supermarket.RESOURCES_PATH}/{_name}/{file_name}', 'r')
                products.update(dict(json.load(_file)))
                _file.close()
                
                # Store fixtures in old fixtures folder.
                if not path.isdir('./old_fixtures'):
                    makedirs('./old_fixtures')
                shutil.move(f'./{file_name}', './old_fixtures/')

        print("Storing product records...", end="")
        supermarket_record = SupermarketModel.objects.get(name=_name.capitalize())
        count:int = 0
        for name, details in products.items():
            count += 1
            if (_name == "picknpay") and (details['discounted_price'] is not None):
                _discounted = details['discounted_price']
            else:
                _discounted = None        
            if details['promo'] == "":
                _promo = None
            else:
                _promo = details['promo']
            product_record = Product(id=f'{supermarket_record.id}{count}',
                                    name=name, price=details['price'], promotion=_promo,
                                    supermarket=supermarket_record, discounted_price=_discounted,
                                    image=details['image'])
            product_record.save()
        print("Done.")

    print("Storage of records completed successfully.")

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

def clean_data(s) -> None:
    _name = s.get_supermarket_name().lower()
    print(f'Cleaning {_name.capitalize()} fixtures...', end='')
    for _file in listdir(f'{s.RESOURCES_PATH}/{_name}/'):
        buffer: dict = {}
        if 'http' in _file:
            file = open(f'{s.RESOURCES_PATH}/{_name}/{_file}', "r")
            prods = dict(json.load(file))
            file.close()
            file = open(f'{s.RESOURCES_PATH}/{_name}/{_file}', 'w')
            for name, data in prods.items():
                price:str = None
                discounted:str = None
                promo:str = None
                image:str = None
                if s.get_supermarket_name() == 'PicknPay':
                    # if there's more than one price in the same field,
                    # move the lesser price to the discounted_price field.
                    if data.get('price').count('R') > 1:
                        sorted = organize_prices(separate_prices(data.get('price')))
                        price = sorted.get('price')
                        discounted = sorted.get('discounted')
                    else:
                        price = data['price']
                    if (data.get('promo') != ""):
                        promo = data.get('promo')
                elif (s.get_supermarket_name() == 'Makro') or (s.get_supermarket_name() == 'Woolworths'):
                    price = data['price'].replace(' ', '')
                    if (data['promo'] != "") and (data['promo'] != None):
                        promo = data['promo']
                else:
                    price = data['price']
                if ((data['image'] != None) and (data['image'] != "")) and ('home' in data['image']):
                    img = Image.open(data['image'].replace('Development Environment/', ''))
                    array_bytes = BytesIO()
                    img.save(array_bytes, 'png')
                    image = base64.b64encode(array_bytes.getvalue()).decode('ascii')
                buffer.update({name: {'price': price, 'discounted_price': discounted, 'promo': promo,
                                        'image': image}})
            json.dump(buffer, file)
            file.close()
    print('complete.\n')

def query_items(query: str, supermarket_name: str = None) -> dict[str]:
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
                if p.discounted_price != None:
                    price = p.discounted_price
                else:
                    price = p.price
                if p.promotion:
                    if check_for_bargain(p.promotion):
                        promotion = p.promotion
                else:
                    promotion = None
                buffer.update({p.name: {'price': price, 'promo': promotion}})
        # discounted products.
        else:
            for s in supermarket.all():
                buffer2: dict[str] = {}
                for p in products:
                    if s.id == p.supermarket_id:
                        if p.discounted_price != None:
                            price = p.discounted_price
                        else:
                            price = p.price
                        if p.promotion:
                            if check_for_bargain(p.promotion):
                                promotion = p.promotion
                        else:
                            promotion = None
                        if p.image:
                            image = p.image
                        else:
                            Common.objects.get(name='Default Product Image')
                        buffer2.update({p.name: {'price': price, 'image': image, 'promo': promotion}})
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
    bargain_substrings = ['FOR', 'Buy', 'BUY', 'for', 'Any', 'any']
    for sub in bargain_substrings:
        if sub in promotion:
            return True
    return False