from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from store.models import Product, Variation, StockVar
from ecart.models import Cart, CartItem
from django.contrib.auth.decorators import login_required

# Create your views here.

def _cart_id(request): # Conseguir la sesion actual
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

# Dictionary index request.POST (es un diccionario): https://stackoverflow.com/questions/4326658/how-to-index-into-a-dictionary
def get_first_key(dictionary):
    for key in dictionary:
        return key
    raise IndexError


def add_prod(request, product_id, flag=False): # ADD_CART course
    
    product = get_object_or_404(Product, id=product_id) # Get the product
    # if the user is authenticated
    current_user = request.user
    if current_user.is_authenticated:
        product_variations = []
        
        if request.method == 'POST':
            option = []
            first_key = get_first_key(request.POST)
            first_val = request.POST[first_key]  # No maneja error si la key no existe en el Dic
            for item in request.POST:  
                key = item
                if key is not first_key:  # Nos saltamos el primer elemento del DicSet
                    # request.POST.get(key, "valor por default")  # Maneja error, devuelve default si key no existe.
                    option = request.POST.get(key)  # key = varcat  value = variation, data-* = stockvar.value
                    value = option.split("-")[0]
                    value_stock = option.split("-")[1] # NO se usó stockvar.value = data-*stockvarvalue, faltó traer data-*                    
                    
                # verificar si la variación coincide con el contenido del modelo (tabla)
                try:
                    #debe ser get(), no filter()           # '__iexact' no importa si son mayusculas o minusculas
                    if len(value_stock) > 0:
                        variations = StockVar.objects.all().filter(product=product_id, variation = Variation.objects.get(variation__iexact=value), value__iexact=value_stock)
                    else:
                        variations = StockVar.objects.all().filter(product=product_id, variation = Variation.objects.get(variation__iexact=value))
                    
                    for var in variations: 
                        product_variations.append(var)
                except:
                    pass


        cart_item_exists = CartItem.objects.filter(product = product, user=current_user).exists()

        if cart_item_exists:
            cart_items = CartItem.objects.filter(product=product, user=current_user) 
            exist_var_list = []
            id_cartitem_list = []
            # Manejo de listas e índices, checar si current_vars are in existing_vars
            for item in cart_items:
                existing_variations = item.variations.all()
                exist_var_list.append(list(existing_variations))
                id_cartitem_list.append(item.id)
            
            if product_variations in exist_var_list:  # Se van recorriendo las dos listas
                index = exist_var_list.index(product_variations)  # obtener el indice de esa variacion
                item_id = id_cartitem_list[index]  # obtener el valor de esa posición del indice
                item = CartItem.objects.get(product=product, id=item_id)
                # Increase cart item quantity
                if flag:
                    item.quantity += 1
                else:
                    if item.quantity > 1:
                        item.quantity -= 1
                item.save()
            else: # Si las variaciones no existen en el cart
                # Create new CartItem item, agregar un nuevo registro a la tabla
                item = CartItem.objects.create(user=current_user, product=product, quantity=1)                
                # Agregar variaciones. Se agregan todos los registros a la tabla, se hace manual.
                item.variations.clear()
                # igual a la iteración: item.variations.add(*product_variations)  # igual a la iteración, * agrega todas:
                if len(product_variations) > 0:
                    for variation in product_variations:
                        item.variations.add(variation) 
                
                item.save()

        else: # Si no existe el CartItem 
            cart_item = CartItem.objects.create(user=current_user, product=product, quantity=1)
            # Agregar variaciones. Se agregan todos los registros a la tabla.
            if len(product_variations) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variations)  # igual a la iteración, *agrega todas:

            cart_item.save()
        return redirect('ecart')
    
    # If user is NOT authenticated
    else:

        product_variations = []
        #if request.POST: No se usa
        if request.method == 'POST':
            option = []
            first_key = get_first_key(request.POST)
            first_val = request.POST[first_key]  # No maneja error si la key no existe en el Dic
            for item in request.POST:  
                key = item
                if key is not first_key:  # Nos saltamos el primer elemento del DicSet
                    option = request.POST.get(key)  # key = varcat  value = variation, data-* = stockvar.value
                    value = option.split("-")[0]
                    value_stock = option.split("-")[1] # NO se usó stockvar.value = data-*stockvarvalue, faltó traer data-*                    

                # verificar si la variación coincide con el contenido del modelo (tabla)
                try:
                    #debe ser get(), no filter()           # '__iexact' no importa si son mayusculas o minusculas
                    if len(value_stock) > 0:
                        variations = StockVar.objects.all().filter(product=product_id, variation = Variation.objects.get(variation__iexact=value), value__iexact=value_stock)
                    else:
                        variations = StockVar.objects.all().filter(product=product_id, variation = Variation.objects.get(variation__iexact=value))
                    
                    for var in variations: 
                        product_variations.append(var)
                except:
                    pass

        try:
            cart = Cart.objects.get(cart_id=_cart_id(request)) # Conseguir el Cart actual con la cart_id de la sesion actual        
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request),
            )
            cart.save()

        cart_item_exists = CartItem.objects.filter(product = product, cart=cart).exists()

        if cart_item_exists: 
            cart_items = CartItem.objects.filter(product=product, cart=cart)
            
            # We need: conseguir como identificar el item que se va a modificar, si no existe: se crea
            # existing_variations <- database
            # current_variations <- product_variations
            # item_id <- database CartItem

            exist_var_list = []
            id_cartitem_list = []
            # Manejo de listas e índices, checar si current_vars are in existing_vars
            for item in cart_items:
                existing_variations = item.variations.all()
                exist_var_list.append(list(existing_variations))
                id_cartitem_list.append(item.id)

            
            if product_variations in exist_var_list:  # Se van recorriendo las dos listas
                index = exist_var_list.index(product_variations)  # obtener el indice de esa variacion
                item_id = id_cartitem_list[index]  # obtener el valor de esa posición del indice
                item = CartItem.objects.get(product=product, id=item_id)
                # Increase cart item quantity
                if flag:
                    item.quantity += 1
                else:
                    if item.quantity > 1:
                        item.quantity -= 1

                item.save()
            else: # Si las variaciones no existen en el cart
                # Create new CartItem item, agregar un nuevo registro a la tabla
                item = CartItem.objects.create(product=product, cart=cart, quantity=1)                
                # Agregar variaciones. Se agregan todos los registros a la tabla, se hace manual.
                item.variations.clear()                
                # igual a la iteración: item.variations.add(*product_variations)  # igual a la iteración, * agrega todas:
                if len(product_variations) > 0:
                    for variation in product_variations:
                        item.variations.add(variation) 
                    
                item.save()

        else: # Si no existen los CartItem 
            cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1)
            # Agregar variaciones. Se agregan todos los registros a la tabla.
            cart_item.variations.clear()
            if len(product_variations) > 0:
                cart_item.variations.add(*product_variations)  # igual a la iteración, *agrega todas:

            cart_item.save()

        return redirect('ecart')

# teclas de aumentar y disminuir cantidad en el carrito
def minus_add_to_prod(request, product_id, cart_item_id, flag=False):        
    try:
        product = get_object_or_404(Product, id=product_id)
        current_user = request.user
        if current_user.is_authenticated:
            cart_item = get_object_or_404(CartItem, id=cart_item_id, product=product, user=current_user)            
        else:    
            cart = get_object_or_404(Cart, cart_id=_cart_id(request))
            cart_item = get_object_or_404(CartItem, id=cart_item_id, product=product, cart=cart)
        # Increase/decrease cart item quantity
        if flag:
            cart_item.quantity += 1
        else:
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
        cart_item.save()
    except:
        pass
    return redirect('ecart')
    

def remove_item(request, product_id, cart_item_id):
    
    try:
        product = get_object_or_404(Product, id=product_id) # Get the product
        
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(id=cart_item_id, product=product, user=request.user) #filtrar las variaciones
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request)) # Conseguir el Cart actual con la cart_id de la sesion actual
            cart_item = CartItem.objects.get(id=cart_item_id, product=product, cart=cart) #filtrar las variaciones
        cart_item.delete()
    except CartItem.DoesNotExist:
        pass
        return redirect('ecart')

    return redirect('ecart')



def ecart(request, total=0, quantity=0, cart_items=None):
    tax = 0
    g_total = 0
    ship_cost = 0
    try:
        sub_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            
        for cart_item in cart_items:
            # el 'price' se obtiene con la recursividad de las clases en los modelos
            #total += cart_item.product.price * cart_item.quantity
            # checar funcion/método def sub_total(request) en el modelo de CartItem
            # cart_item.sub_total -> una instancia, cart_item.sub_total() -> valor resultante, 
            sub_total = cart_item.sub_total()   # checa si tiene descuento el price
            total +=  sub_total
            quantity += cart_item.quantity
        
        # Revisar si aplica esto para vendedores nacionales
        ship_cost = 99   # Crear tabla para tax y para ship_cost (por zonas por estados calcular tarifa)
        ship_total = total + ship_cost
        tax = (2 * total)/100
        
        g_total = ship_total # debería ser si se cobran impuestos: g_total = ship_total + tax
    except Cart.DoesNotExist or CartItem.DoesNotExist:
        pass
    context = {
    'total': total,
    'tax': tax,
    'ship_cost': ship_cost,
    'g_total': g_total,
    'quantity': quantity,
    'cart_items': cart_items,
    }
    return render(request, 'store/ecart.html', context)
    
        

@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    tax = 0
    g_total = 0
    ship_cost = 0
    try:
        sub_total = 0
        sub_total = None

        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        
        for cart_item in cart_items:
            # el 'price' se obtiene con la recursividad de las clases en los modelos
            #total += cart_item.product.price * cart_item.quantity
            # checar funcion/método def sub_total(request) en el modelo de CartItem
            # cart_item.sub_total = una instancia, cart_item.sub_total() -> valor resultante, 
            cart_price = 0
            sub_total = cart_item.sub_total()
            total +=  sub_total
            quantity += cart_item.quantity
            cart_price = cart_item.cartitem_price()
            cart_item.price = cart_price
            cart_item.save()
        
        # Revisar si aplica esto para vendedores nacionales
        ship_cost = 99
        ship_total = total + ship_cost
        tax = (2 * total)/100
        g_total = ship_total # debería ser si se cobran impuestos: g_total = ship_total + tax
    except Cart.DoesNotExist or CartItem.DoesNotExist:
        pass
    context = {
    'total': total,
    'tax': tax,
    'ship_cost': ship_cost,
    'g_total': g_total,
    'quantity': quantity,
    'cart_items': cart_items,
    }
    return render(request, 'store/checkout.html', context)