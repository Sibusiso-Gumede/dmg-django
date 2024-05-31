from django.shortcuts import render
from dmg_django_app.modules.transformation.data_io import query_items
from dmg_django.settings import GOOGLE_API_KEY
from dmg_django_app.modules.common import Supermarkets

def homepage(request):
    """The home page for the dmg_django_app."""
    return render(request, 'dmg_django_app/home.html')

def receiptify(request):
    """Generates slips of the listed products."""
    
    context: dict = {}
    s_names: list[str] = []
    s_choice: str = ""
    
    for supermarket in Supermarkets.SUPERMARKETS.values():
        s_names.append(supermarket.get_supermarket_name())
    
    context.update({'supermarket_names': s_names, 'query': False})

    if not (request.META.get('QUERY_STRING') == ''):
        s_choice = request.GET.get('supermarket-choice')
        context['query'] = True
        context.update({'products': query_items(request.GET.get('typeToAddProduct'), s_choice)})

    return render(request, 'dmg_django_app/receiptify.html', context)

def discounted_products(request):
    """Generate content for the different products their prices."""

    context = {}
    return render(request, 'dmg_django_app/discounted_products.html', context)

def near_me(request):
    """Displays supermarkets near the user."""
    query_substring:str = ""
    for supermarket in Supermarkets.SUPERMARKETS.values():
        query_substring += supermarket.get_supermarket_name()+'+'
    context = {"source": f"https://www.google.com/maps/embed/v1/search?key={GOOGLE_API_KEY}&q={query_substring}in+Standerton,+Mpumalanga"}
    return render(request, 'dmg_django_app/near_me.html', context)