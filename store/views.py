from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.urls import reverse

from store.models import Product, VarCat, Variation, StockVar
from category.models import Category, SubCategory
from ecart.models import Cart, CartItem
from ecart.views import _cart_id

# Create your views here.
"""
def get_variations(product):
    
    return HttpResponse(f"dentro de get_variations")
    try:
        return HttpResponse(f"entra a try: de _get_vars")
        varsall = StockVar.objects.all()
        return HttpResponse(f"Variaciones: {varsall} {product}")
    except Exception as e:
        raise e
    
    return HttpResponse(f"No pasa try: de _get_vars")
    return varsall
"""

def paging(request, products, number_pages):
    paginator = None
    page = None
    paged_products = None
    paginator = Paginator(products, number_pages)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    return paged_products

def store(request, category_slug=None):
    paged_products = None
    products = None
    low_prods = None

    if category_slug != None:
        category = get_object_or_404(SubCategory, slug=category_slug)
        products = Product.objects.filter(categories=category, is_available=True).order_by('-has_discount', '-created_at')
        prod_count = products.count()

        low_prods = Product.objects.filter(categories=category, is_available=True, has_discount=True)
        low_prod_count = low_prods.count()
        
        #paged_products = paging(request, products, 1)

    else:
        products = Product.objects.all().filter(is_available=True).order_by('-has_discount', '-created_at')
        prod_count = products.count()

        low_prods = Product.objects.filter(is_available=True, has_discount=True)
        low_prod_count = low_prods.count()

    if products:    
        paged_products = paging(request, products, 3)
    
    context = {
        'title': 'Store',
        'products': paged_products,
        'prod_count': prod_count,
        'low_prod_count': low_prod_count,
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    varsall = None
    try:              # con doble '__' se hace recursivo a parámetro de un campo 'foreign key'
        single_product = Product.objects.get(categories__slug=category_slug, slug=product_slug)
        subcat = SubCategory.objects.get(slug=category_slug)

        varsall = StockVar.objects.all().filter(product = single_product).order_by('variation__varcat')
        #Prefetch Foreign https://stackoverflow.com/questions/76143776/django-template-language-how-to-write-model-model-set-filter-in-a-template
        #https://forum.djangoproject.com/t/how-to-filter-this-manytomany-relation/6451
        #followed_posts = Posts.objects.filter(autor__followers__username=user_username)
        #catsall = VarCat.objects.all().filter(varcat in varsall)
        #catall = Variation.objects.all().filter(variation=)
        #catall = VarCat.objects.all().filter(varcat = varsall__variations)
        #todasvar = Variation.objects.filter(variation=indexstock)
        #varsall = get_variations(single_product)

        # no regresa un objeto del query_set, solo el valor booleano            
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
        
        
        #return HttpResponse(f"dentro de Try: product_detail, no entra a la función")
    except Exception as e:
        raise e
    
    context = {
            'prod': single_product,
            'cat': subcat.category,
            'subcat': subcat,
            'in_cart': in_cart,
            'varsall': varsall,
    }
    #return render(request, "store/product_detail_1.html", context)  # Sin variaciones
    return render(request, "store/product_detail_vars.html", context) # OK


def search(request):
    description = None
    name = None
    products = None
    paged_products = None
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']

        if keyword:  # si no está vacío el input name="keyword" en GET
            """
            description = Product.objects.order_by('-has_discount', '-created_at').filter(description__icontains=keyword, is_available=True)
            name = Product.objects.order_by('-has_discount', '-created_at').filter(name__icontains=keyword, is_available=True)
            # Esta opcion era el mismo resultado: products = description | name
            """
            products = Product.objects.filter(
                Q(description__icontains=keyword) | Q(name__icontains=keyword)
                ).order_by('-has_discount', '-created_at')
            prod_count = products.count()

            low_prods = products.filter(has_discount=True)
            low_prod_count = low_prods.count()
            
        else: 
            products = Product.objects.order_by('-has_discount', '-created_at').filter( is_available=True)
            prod_count = products.count()
            low_prods = Product.objects.order_by('-has_discount', '-created_at').filter(is_available=True, has_discount=True)
            low_prod_count = low_prods.count()
            
        paged_products = paging(request, products, 2)
        context = {
            'products': paged_products,
            'prod_count': prod_count,
            'low_prod_count': low_prod_count,
        }
        
        return render(request, 'store/store.html', context)

     