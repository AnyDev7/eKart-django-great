from django import forms
from .models import Account

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'nuevo contraseña',
        'class': 'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'confirma contraseña',
        'class': 'form-control',
    }))
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
        
# Form validation Bootstrap: https://getbootstrap.com/docs/5.0/forms/validation/