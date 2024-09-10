import django
from os import environ

environ.setdefault("DJANGO_SETTINGS_MODULE", "dmg_django.settings")
django.setup()

from . import Scraper


def scrape(super):
    s = Scraper(super)
    s.scrape_products()