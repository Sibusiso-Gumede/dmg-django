"""Defines URL patterns for dmg_django_app."""

from django.urls import include, path
from . import views

urlpatterns = [
    # Home page
    path(r'', views.groceryItemsForm, name='home'),
    # Grocery slips page.
    path(r'grocery_slips/', views.generateSlips, name='generateSlips'),
    # Best discounted products.
    path(r'best_discounted_products/', views.bestDiscountedProducts, name='bestdiscounted'),
]