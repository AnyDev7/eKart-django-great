import json
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404

from ecart.models import CartItem
from .forms import OrderForm
from .models import Order, Payment, OrderProduct
from store.models import Product
from account.models import Address

import datetime
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.http import JsonResponse

# Create your views here.

def payment(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        print("Body: ", body)
        order = get_object_or_404(Order, user=request.user, is_ordered=False, number=body['orderID'])
        print("Orden: ", order)
        try:
            # store transaction data
            payment = Payment(
                user = request.user,
                payment_id = body['transID'],
                payment_method = body['payment_method'],
                amount_paid = order.total,  #float(body['payment_amount']), #Order model: order.total
                #currency = body['payment_currency'], # Aún no queda el POST en el script de payment.html
                status = body['status'],
            )
            payment.save()
            
            order.payment = payment  # Foreign_key se asigna el objeto completo al campo ForeignKey
            order.is_ordered = True
            order.status = "Pagada"
            order.save()

            # Move cart items to OrderProduct table 
            cart_items = CartItem.objects.filter(user=request.user)
            for item in cart_items:
                orderproduct = OrderProduct()
                orderproduct.order_id = order.id
                orderproduct.payment = payment
                orderproduct.user_id = request.user.id
                orderproduct.product_id = item.product_id
                orderproduct.quantity = item.quantity
                orderproduct.price = item.price
                orderproduct.ordered = True
                orderproduct.save()

                cart_item = CartItem.objects.get(id=item.id)
                product_variations = cart_item.variations.all()
                orderproduct = OrderProduct.objects.get(id=orderproduct.id)
                orderproduct.variations.set(product_variations)
                orderproduct.save()

                # decrease o reduce quantity of sale product & variation
                product = Product.objects.get(id=item.product_id)
                product.stock -= item.quantity
                product.save()  # Hasta aqui OK

                # Decrease quantity of variation
                for stockvar in product_variations:
                    stockvar.stock -= item.quantity
                    stockvar.save()
            
            # Clear Cart
            CartItem.objects.filter(user=request.user).delete()

            # Send Order recieved email to customer
            mail_subject = '¡Gracias por tu compra!'
            mail_message = render_to_string('order/order_recieved_email.html', {
                'user': request.user,
                'order': order,
                'cart_items': cart_items,
                'company': 'AP Equipos Integrados SA CV',
            })
            to_email = request.user.email
            send_email = EmailMessage(mail_subject, mail_message, to=[to_email])
            send_email.send()

            # Send order number and transaction id back to sendData method via JsonResponse
            data = {
                'order_number': order.number,
                'payment_id': payment.payment_id,
                #Sí funciona: 'status': order.status,
                #Sí funciona: 'date': order.created_at,
            }

        except:
            None

    return JsonResponse(data)


def place_order(request, shipment_option, address_id=None, total=0, quantity=0):
    current_user = request.user
    cart_count = 0
    ship_cost = 99  # Crear tabla para tax y para ship_cost (por zonas por estados calcular tarifa)
    tax = 0 #Cálculo de impuestos: (2 * total)/100
    sub_total = 0
    g_total = 0
    address = None

    try:
        cart_items = CartItem.objects.filter(user=current_user)
        cart_count = cart_items.count()
    except:
        if cart_count <= 0:
            return redirect('store')
    
    if shipment_option == 'pickup':
        ship_cost = 0
    else:
        try:
            address = Address.objects.get(id=address_id)
        except Address.DoesNotExist:
            return redirect('store')
    
    for cart_item in cart_items:
        cart_price = 0
        # Aqui se puede verificar si el precio sigue siendo de promocion.
        sub_total = cart_item.sub_total()
        total +=  sub_total  # Total de productos
        quantity += cart_item.quantity
        # Aqui se puede verificar si el precio sigue siendo de promocion.
        cart_price = cart_item.cartitem_price()
        cart_item.price = cart_price
        cart_item.save()

    
    ship_total = total + ship_cost
    g_total = ship_total + tax # debería ser si se cobran impuestos: g_total = ship_total + tax

    if request.method == 'POST':
        """
        # Borrar: Cómo iterar un request.POST
        post = []
        for key in request.POST:
            post.append(request.POST[key])
        return HttpResponse(post)
        # Borrar
        """

        form = OrderForm(request.POST)
        if form.is_valid():
            try:
                data = Order()
                data.user = current_user
                data.first_name = form.cleaned_data['first_name']
                data.last_name = form.cleaned_data['last_name']
                data.phone = form.cleaned_data['phone']
                data.email = form.cleaned_data['email']
                if shipment_option == "pickup":
                    data.shipment = False
                    data.address_line_1 = "cliente retira en nuestra bodega"
                    data.address_line_2 = "cliente retira en nuestra bodega"
                    data.country = ""
                    data.state = ""
                    data.city = ""
                    data.zipcode = ""
                else:
                    data.address_line_1 = address.address_line_1
                    data.address_line_2 = address.address_line_2
                    data.country = address.country
                    data.state = address.state
                    data.city = address.city
                    data.zipcode = address.zipcode
                data.note = form.cleaned_data['note']
                data.sub_total = total # total de productos antes de envio e impuestos
                data.ship_cost = ship_cost                
                data.tax = tax
                data.total = g_total
                data.status = "Recibida"
                data.ip = request.META.get('REMOTE_ADDR')
                data.save()

                # Generate order number
                yr = int(datetime.date.today().strftime('%Y'))
                dt = int(datetime.date.today().strftime('%d'))
                mt = int(datetime.date.today().strftime('%m'))
                d = datetime.date(yr, mt, dt)
                current_date = d.strftime('%Y%m%d') #20240611
                
                # Rellenar de ceros 5 espacios
                id_len = len(str(data.id))
                zeros = ''  # inicializar con 1 '0', para que agregue los ceros indicados
                if id_len < 6:                
                    for i in range(6-id_len):
                        zeros += '0'
                    order_number = current_date + zeros + str(data.id)
                else:
                    order_number = current_date + str(data.id)
                
                data.number = order_number
                data.save()
            except:
                None

            # Orden generada (que esta en DB) enviar a template para PAGO
            order = get_object_or_404(Order,user=current_user, number=order_number, is_ordered=False)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'ship_cost': ship_cost,
                'tax': tax,
                'g_total': g_total,
                'ship_total': ship_total,
            }
            return render(request, 'order/payment.html', context)
        else:
            return HttpResponse('La forma no es válida')
    else:
        return redirect('checkout')

def order_complete(request):
    order_number = request.GET.get('order_number')
    payment_id = request.GET.get('payment_id')
    try:
        order = Order.objects.get(number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        payment = Payment.objects.get(payment_id=payment_id)
        context = {
            'order': order,
            'ordered_products': ordered_products,
            'payment': payment,
        }
        return render(request, "order/order_complete.html", context)
    
    except (Payment.DoesNotExist, Order.DoesNotExist):
        None #return redirect('home')

    

"""
#ManytoMany https://docs.djangoproject.com/en/5.0/topics/db/examples/many_to_many/
# MODELS

class Publication(models.Model):
    title = models.CharField(max_length=30)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Article(models.Model):
    headline = models.CharField(max_length=100)
    publications = models.ManyToManyField(Publication)

    class Meta:
        ordering = ["headline"]

    def __str__(self):
        return self.headline

# VIEW
# crear dirección
p1 = Publication(title="The Python Journal")
p1.save()
# crear usuario
a1 = Article(headline="Django lets you build web apps easily")
a1.save() # Si usuario ya existe, se omite
# Asociar dir a user / agregar una direccion a usuario
a1.publications.add(p1)
"""

