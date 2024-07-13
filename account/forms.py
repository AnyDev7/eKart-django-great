from django import forms
from .models import Account, UserProfile

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'nuevo contraseña',
        'class': 'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'confirma contraseña',
        'class': 'form-control',
    }))

# Borrar, es para Mesas de FoodTruck App
    CHOICES = {"1": "First", "2": "Second"} # Borrar
    choice_field = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES) # Borrar
    
    TABLES = ( # Borrar
        ("AUT", "Mesa 1"),
        ("DEU", "Mesa 2"),
        ("NLD", "Mesa 3"),
    )
    tables = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=TABLES) # Borrar

    class Meta:
        model = Account
        # campos que serán REQUERIDOS = Obligatorios en el Form
        fields = ['first_name', 'last_name', 'phone', 'email', 'password', 'city', 'country']
    
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'ingresa tu nombre'
        self.fields['last_name'].widget.attrs['placeholder'] = 'ingresa tus apellidos'
        self.fields['email'].widget.attrs['placeholder'] = 'ingresa correo'
        self.fields['phone'].widget.attrs['placeholder'] = 'ingresa tu telefono'
        self.fields['city'].widget.attrs['placeholder'] = 'ingresa tu ciudad'
        self.fields['country'].widget.attrs['placeholder'] = 'ingresa tu pais'
        self.fields['country'].widget.attrs['value'] = 'México'
        for x in self.fields:
            self.fields[x].widget.attrs['class'] = 'form-control'
    
    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        
class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'phone', 'city', 'state', 'country')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        #self.fields['first_name'].widget.attrs['placeholder'] = 'ingresa tu nombre'
        #self.fields['last_name'].widget.attrs['placeholder'] = 'ingresa tus apellidos'
        #self.fields['phone'].widget.attrs['placeholder'] = 'ingresa tu telefono'
        #self.fields['city'].widget.attrs['placeholder'] = 'ingresa tu ciudad'
        #self.fields['country'].widget.attrs['placeholder'] = 'ingresa tu pais'
        #self.fields['country'].widget.attrs['value'] = 'México'
        for x in self.fields:
            self.fields[x].widget.attrs['class'] = 'form-control'

class UserProfileForm(forms.ModelForm):
    picture = forms.ImageField(required=False, error_messages={'invalid':("Solo archivos de imagen")}, widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields = ('picture',)

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for x in self.fields:
            self.fields[x].widget.attrs['class'] = 'form-control'

# Form validation Bootstrap: https://getbootstrap.com/docs/5.0/forms/validation/