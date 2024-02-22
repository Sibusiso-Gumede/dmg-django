from django.shortcuts import render

def groceryItemsForm(request):
    """The home page for the dmg_django_app."""
    return render(request, 'dmg_django_app1/home.html')

def bestCategoryProducts(request):
    """The page that displays products in different categories."""
    return render(request, 'dmg_django_app1/categoryProducts.html')

def bestDiscountedProducts(request):
    """The page for displaying products with the highest discount."""
    return render(request, 'dmg_django_app1/discountedProducts.html')