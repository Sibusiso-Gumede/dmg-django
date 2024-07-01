"""Defines URL patterns for dmg_django_app."""

from django.urls import include, path
from .views import *

urlpatterns = [
    # Home page
    path('', homepage, name='home'),
    # Receipt renderer page.
    path('receiptify/', receiptify, name='receiptify'),
    # Discounted products page.
    path('home/discounted_products/', discounted_products, name='discounted_products'),
    # Nearby supermarkets page.
    path('near_me/', near_me, name='near_me'),
    # Autosuggestions url.
    path('autosuggestion/', product_autosuggestion, name='product_autosuggestion'),
    # Receipt rendering url.
    path('get_receipt/', get_receipt, name='get_receipt'),
]