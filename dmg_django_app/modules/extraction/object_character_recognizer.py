"""This module extracts text from image objects."""

from pytesseract import image_to_string
from transformation import Image, retrieve_image, resize_image, map_function, listdir
from supermarket_apis import Supermarket, Spar

def product_details_ocr(supermarket: Supermarket):
    images = retrieve_image(supermarket.get_images_path())
    results = map_function(resize_image, images)
    for result in results:
        print(image_to_string(result))

if __name__ == '__main__':
    spar = Spar()
    product_details_ocr(spar)