from django.shortcuts import render
from dmg_django_app.modules.transformation.data_io import query_items

def homepage(request):
    """The home page for the dmg_django_app."""
    return render(request, 'dmg_django_app/home.html')

def receiptify(request):
    """Generates slips of the listed products."""

    context = {}
    return render(request, 'dmg_django_app/receiptify.html', context)

def discounted_products(request, **kwargs):
    """Generate content for the different products their prices."""

    context = {}
    return render(request, 'dmg_django_app/discounted_products.html', context)

def near_me(request):
    """Displays supermarkets near the user."""
    return render(request, 'dmg_django_app/near_me.html')