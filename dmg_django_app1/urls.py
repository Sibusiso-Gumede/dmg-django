"""Defines URL patterns for dmg_django_app1."""

from django.urls import path
from . import views

urlpatterns = [
    # Home page
    path(r'', views.groceryItemsForm, name='home'),
    # Category products page.
    path(r'category_products/', views.bestCategoryProducts, name='categories'),
    # Best discounted products.
    path(r'best_discounted_products/', views.bestDiscountedProducts, name='bestdiscounted'),
]