from django.shortcuts import render, HttpResponse, redirect, get_object_or_404


from .forms import RegisterForm, UserForm, UserProfileForm
from .models import Account, UserProfile
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from ecart.models import Cart, CartItem
from ecart.views import _cart_id

# User verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from order.models import Order, OrderProduct

# * VERIFICAR ESTA LIBRERIA
import requests

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            city = form.cleaned_data['city']
            country = form.cleaned_data['country']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone = phone
            user.city = city
            # obtener el valor seleccionado del select: key & value con request.POST
            user.state = request.POST['inputState'] # hace referencia la 'key' al 'name' del select o input
            user.country = country
            
            """ Checar USUARIO REGISTRADO NO ACTIVADO
            check_user = get_object_or_404(Account, email=email)
            if check_user.email == email and not check_user.is_active:
                return HttpResponse("El usuario existe, pero NO esta inactivo")
            """
            user.save()
            # Create User Profile
            profile = UserProfile()
            profile.user_id = user.id
            profile.picture = 'default/no_gender_user_profile_picture.png'
            profile.save()

            # User activation
            current_site = get_current_site(request)
            mail_subject = '¡Bienvenido!, ahora activa tu cuenta'
            mail_message = render_to_string('account/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
                'company': 'AP Equipos Integrados SA CV',
            })
            to_email = email
            send_email = EmailMessage(mail_subject, mail_message, to=[to_email])
            send_email.send()
            
            #messages.success(request, "Se creo tu usuario, revisa tu correo para activar tu cuenta.")

            return redirect('/account/login/?command=verification&email='+email) # Revisar si se deja este return
        #else:            
        #    return HttpResponse(form.errors)
    else:
        # Solo limpia la Form si es la primera vez que se accesa, si o muestra errores y contenido de form
        form = RegisterForm()  
    states_mx = [
        'Aguascalientes',
        'Baja California',
        'Baja California Sur',
        'Campeche',
        'Chiapas',
        'Chihuahua',
        'Ciudad de México',
        'Coahuila de Zaragoza',
        'Colima',
        'Durango',
        'Estado de México',
        'Guanajuato',
        'Guerrero',
        'Hidalgo',
        'Jalisco',
        'Michoacán de Ocampo',
        'Morelos',
        'Nayarit',
        'Nuevo León',
        'Oaxaca',
        'Puebla',
        'Querétaro',
        'Quintana Roo',
        'San Luis Potosí',
        'Sinaloa',
        'Sonora',
        'Tabasco',
        'Tamaulipas',
        'Tlaxcala',
        'Veracruz de Ignacio de la Llave',
        'Yucatán',
        'Zacatecas'
        ]
    context = {
        'form': form,
        'states_mx': states_mx,
    }
    return render(request, 'account/register.html', context)


def login(request):
    if request.method == 'POST':        
        email = request.POST['email']
        password = request.POST['password']

        # Auntenticar el usuario capturado en el form
        user = auth.authenticate(email=email, password=password) 

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id= _cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_items = CartItem.objects.filter(cart=cart)

                    # getting the product variartions by cart id
                    product_variations = []
                    for item in cart_items:
                        variations = item.variations.all()
                        product_variations.append(list(variations))

                    #Get the cart items from the user to access his product variations
                    cart_items = CartItem.objects.filter(user=user) 
                    exist_var_list = []
                    id_cartitem_list = []
                    for item in cart_items:
                        existing_variations = item.variations.all()
                        exist_var_list.append(list(existing_variations))
                        id_cartitem_list.append(item.id)
                    # Get common variations in 2 list: product_variations & exist_var_list
                    for pr in product_variations:
                        if pr in exist_var_list:
                            index = exist_var_list.index(pr)
                            item_id = id_cartitem_list[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_items = CartItem.objects.filter(cart=cart)
                            for item in cart_items:
                                item.user = user
                                item.save()
                    #auth.login(request, user) # Agregado por mi Sí funciona
                    #messages.success(request, "Bienvenido a pagar tu orden, pero primero tus datos")
                    #return redirect('checkout') # Agregado por mi Sí funciona
            except:
                pass
            auth.login(request, user)
            messages.success(request, "Bienvenido a tu cuenta")
            url = request.META.get('HTTP_REFERER')
            #messages.success(request, url) # Quitar
            try:
                query = requests.utils.urlparse(url).query
                # looking for ej => 'next=/cart/checkout/'
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    next_page = params['next']
                    messages.success(request, "Para pagar tu orden, revisa tus datos")
                    return redirect(next_page)
            except:
                return redirect('dashboard')
        else:
            messages.error(request, "Correo + contraseña no validos")
            return redirect('login')
    return render(request, 'account/login.html')


@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request,"¡Saliste de tu cuenta!")

    return redirect('login')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode() # = user.id  (desencriptar)
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Felicidades, tu cuenta ha sido activada.')
        return redirect('login')
    else:
        messages.error(request, 'Liga de activación invalida, inténtelo de nuevo.')
        return redirect('register')  # CHECAR, si se genera nueva liga (link) de activación.
    

@login_required(login_url = 'login')
def dashboard(request):
    try:
        orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
        orders_count = orders.count()
        userprofile = get_object_or_404(UserProfile, user_id=request.user.id)
        context = {
            'orders_count': orders_count,
            'userprofile': userprofile,
        }
    except:
        None
    return render(request, 'account/dashboard.html', context)


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():           
            user = Account.objects.get(email__exact=email)
            
            # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reinicia la contraseña de tu cuenta'
            mail_message = render_to_string('account/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
                'company': 'AP Equipos Integrados SA CV',
            })
            to_email = email
            send_email = EmailMessage(mail_subject, mail_message, to=[to_email])
            send_email.send()
            
            messages.success(request, "Se ha enviado el correo para generar una nueva contraseña, revisa tu correo.")

            return redirect('login')
        else:            
            messages.error(request, "No existe cuenta con ese correo, revisa que sea correcto.")

    return render(request, 'account/forgot_password.html')


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode() # = user.id  (desencriptar)
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        # guardar el uid de la sesión.
        request.session['uid'] = uid
        messages.success(request, 'Por favor crea tu nueva contraseña.')
        # enviarlo a otra form para capturar nuevo correo
        return redirect('reset_password')
    else:
        messages.error(request, 'Liga de activación invalida, inténtelo de nuevo.')
        return redirect('forgot_password')
    

def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')
            user = get_object_or_404(Account, pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, "Las contraseña se ha cambiado exitosamente.")
            return redirect('login')
        else:
            messages.error(request, "Las contraseñas deben ser iguales")
        
    return render(request, 'account/reset_password.html')


@login_required(login_url='login')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user_id=request.user.id)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user) # 'instance' es para editar la instancia que ya existe
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Tu datos de perfil se actualizaron.')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user) # 'instance' es para editar la instancia que ya existe
        profile_form = UserProfileForm(instance=userprofile)
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'userprofile': userprofile,
        }
        return render(request, 'account/edit_profile.html', context)


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        user = get_object_or_404(Account, username__exact=request.user.username )
        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Se cambio con éxito su contraseña.')
                auth.logout(request)
                return redirect('login')
            else:
                messages.error(request, 'Contraseña actual incorrecta.')
        else:
                messages.error(request, 'Nueva constraseña no coincide.')
        return redirect('change_password')
    
    return render(request, "account/change_password.html")


@login_required(login_url='login')
def my_orders(request):
    try:
        orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
        # Unir o sumar queryset's : https://stackoverflow.com/questions/29587382/how-to-add-an-model-instance-to-a-django-queryset
        orderproducts = OrderProduct.objects.filter(user__id=request.user.id, ordered=True)
        context = {
            'orders': orders,
            'orderproducts': orderproducts,
        }
    except:
        None
    return render(request, "account/my_orders.html", context)


@login_required(login_url='login')
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    ordered_products = OrderProduct.objects.filter(order__id=order_id) # order__id: doble 'underscore' para accesar al campo de foreignkey
    context = {
        'order': order,
        'ordered_products': ordered_products,
    }
    return render(request, 'order/order_detail.html', context)