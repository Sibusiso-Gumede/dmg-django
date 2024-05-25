"""Defines URL patterns for dmg_django_app."""

from django.urls import include, path
from . import views

urlpatterns = [
    # Home page
    path('', views.homepage, name='home'),
    # Receipt renderer page.
    path('home/receiptify', views.receiptify, name='receiptify'),
    # Discounted products page.
    path('home/discounted_products/', views.discounted_products, name='discounted_products'),
    # Nearby supermarkets page.
    path('home/near_me', views.near_me, name='near_me')
]