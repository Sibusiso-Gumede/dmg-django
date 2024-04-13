# Transformation and loading module for managing data.

import json

from io import BytesIO
from PIL import Image, UnidentifiedImageError
from django.core.files.base import File
from os import path, listdir, makedirs
from ..supermarket_apis import Supermarket
from ...models import Supermarket as SupermarketModel, Product
   
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

def store_supermarket_records(s:Supermarket) -> File:
    s_name = s.get_supermarket_name()
    file = f'{s.RESOURCES_PATH}/{s_name}/{s_name}_products.json'
    if not path.isfile(file):
        raise FileNotFoundError   
    with open(file, 'r') as f:
        items:dict = json.load(f)                          
        supermarket_record = SupermarketModel(id=s.identifier,
                                            name=s.get_supermarket_name(),
                                            num_of_products=len(list(items.keys())))
        supermarket_record.save()
        return File(f)

def store_product_records(supermarket_name: str, file: File) -> None:
    supermarket_record = SupermarketModel.objects.get(supermarket_name=supermarket_name)
    count:int = 0
    for name, data in dict(json.load(file)).items():
        count += 1
        product_record = Product(id=int(f'{supermarket_record.id}{count}'),
                                name=name, price=data['price'], promotion=data['promo'],
                                supermarket=supermarket_record)
        product_record.save()