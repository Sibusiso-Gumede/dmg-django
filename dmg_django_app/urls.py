"""Defines URL patterns for dmg_django_app."""

from django.urls import include, path
from . import views

urlpatterns = [
    # Home page
    path('', views.homepage, name='home'),
    # Grocery slips page.
    path('home/receiptify', views.receiptify, name='receiptify'),
    # Best discounted products.
    path('home/discounted_products/', views.discounted_products, name='discountedproducts'),
]