from django.shortcuts import HttpResponse, render
from store.models import Product, Rating

# Create your views here.

def home(request):
    
    products = Product.objects.all().filter(is_available=True).order_by( '-created_at', '-has_discount')
    for product in products:
        ratings = Rating.objects.filter(product_id=product.id, status=True)

    context = {
        'title': "Listado productos",
        'products': products,
        'ratings': ratings,
    }
    return render(request, 'mainapp/home.html', context) # 'mainapp' subdirectorio en 'templates'