from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('Usuario requiere un correo')
        if not username:
            raise ValueError('Usuario debe tener un nombre de usuario')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, first_name, last_name, username, email, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
            password = password,
        )
        
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user
    

class Account(AbstractBaseUser):
    first_name = models.CharField('Nombre(s)', max_length=50)
    last_name = models.CharField('Apellidos', max_length=50)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField('Email', max_length=100, unique=True)
    phone_number = models.CharField(max_length=50)
    city = models.CharField('Ciudad', max_length=50, default="")
    state = models.CharField('Estado', max_length=50, default="")
    country = models.CharField('Pais', max_length=50, default="")

    # requeridos
    joined_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager() # la clase del modelo que declaramos al inicio 

    class Meta:
        verbose_name = 'cuenta de usuario'
        verbose_name_plural = 'cuentas de usuario'
    
    def __str__(self):
        return f"{self.username} - {self.email}"
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

    #models.PhoneNumberField(_(""))
    #models.EmailField(_(""), max_length=254)