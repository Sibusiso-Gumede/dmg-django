from django.shortcuts import render

def groceryItemsForm(request):
    """The home page for the dmg_django_app."""
    return render(request, 'dmg_django_app/index.html')

def generateSlips(request):
    """The page generates slips of the listed products."""
    return render(request, 'dmg_django_app/grocerySlips.html')

def bestDiscountedProducts(request):
    """The page for displaying products with the highest discount."""
    return render(request, 'dmg_django_app/discountedProducts.html')