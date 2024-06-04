from django.shortcuts import render
from django.http import JsonResponse
from dmg_django_app.modules.transformation.data_io import query_items
from dmg_django.settings import GOOGLE_API_KEY
from dmg_django_app.modules.common import Supermarkets

context = {"supermarket_names": [
    Supermarkets.CHECKERS, Supermarkets.MAKRO,
    Supermarkets.PNP, Supermarkets.SHOPRITE,
    Supermarkets.WOOLIES
]}

def product_auto_suggestion(request):
    products: list[str] = []
    for item in query_items(request.GET.get('term'), request.GET.get('supermarket-choice')):
        products.append(item)
    return JsonResponse(products, safe=False)

def homepage(request):
    """The home page for the dmg_django_app."""
    return render(request, 'dmg_django_app/home.html')

def receiptify(request):
    """Generates slips of the listed products."""
    return render(request, 'dmg_django_app/receiptify.html', context)

def discounted_products(request):
    """Generate content for the different products their prices."""
    return render(request, 'dmg_django_app/discounted_products.html', context)

def near_me(request):
    """Displays supermarkets near the user."""
    query_substring:str = ""
    for supermarket in context.get('supermarket_names'):
        query_substring += supermarket+'+'
    query_substring = query_substring[:-2] #remove trailing plus sign.
    return render(request, 'dmg_django_app/near_me.html', {"source": f"https://www.google.com/maps/embed/v1/search?key={GOOGLE_API_KEY}&q={query_substring}"})