import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from dmg_django.settings import GOOGLE_API_KEY
from dmg_django_app.modules.transformation.data_io import query_items, receipt
from dmg_django_app.modules.common import Supermarkets

context = {"supermarket_names": [
    Supermarkets.CHECKERS, Supermarkets.MAKRO,
    Supermarkets.PNP, Supermarkets.SHOPRITE,
    Supermarkets.WOOLIES
]}

def product_autosuggestion(request):    
    return JsonResponse(query_items(request.GET.get('type-to-add'), request.GET.get('supermarket-choice')), safe=True)

def homepage(request):
    """The home page for the dmg_django_app."""
    return render(request, 'dmg_django_app/home.html')

def receiptify(request):
    """Display an interface for the user to choose products."""
    return render(request, 'dmg_django_app/receiptify.html', context)

def discounted_products(request):
    """Generate the product content of the searched product across all supermarkets."""
    context = query_items(request.GET.get('searchBox'))
    return render(request, 'dmg_django_app/discounted_products.html', context)

def near_me(request):
    """Displays supermarkets near the user."""
    query_substring:str = ""
    for supermarket in context.get('supermarket_names'):
        query_substring += supermarket + '+'
    query_substring = query_substring[:-2] #remove trailing plus sign.
    return render(request, 'dmg_django_app/near_me.html', {"source": f"https://www.google.com/maps/embed/v1/search?key={GOOGLE_API_KEY}&q={query_substring}"})

def get_receipt(request):
    """Generates slips of the listed products."""
    return JsonResponse(receipt(json.loads(request.body)), safe=True)