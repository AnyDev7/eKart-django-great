from django.shortcuts import HttpResponse, render
from store.models import Product

# Create your views here.

def home(request):
    
    products = Product.objects.all().filter(is_available=True)

    context = {
        'title': "Listado productos",
        'products': products,
    }
    #return HttpResponse('<h1>Pagina de inicio</h1>')
    return render(request, 'mainapp/home.html', context) # 'mainapp' subdirectorio en 'templates'