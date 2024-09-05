import django
from . import Scraper
from os import environ

environ.setdefault("DJANGO_SETTINGS_MODULE", "dmg_django.settings")
django.setup()

def scrape(super):
    s = Scraper()
    s.scrape_products(super)