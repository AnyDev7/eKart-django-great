from django.shortcuts import render, HttpResponse, redirect, get_object_or_404


from .forms import RegisterForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

# User verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            city = form.cleaned_data['city']
            country = form.cleaned_data['country']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
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

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "Bienvenido a tu cuenta")
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
    return render(request, 'account/dashboard.html')


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