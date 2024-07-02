from django.db import models
from category.models import Category, SubCategory
from django.urls import reverse


# Create your models here.


class VarCat(models.Model):
    varcat = models.CharField('Catálogo variación', max_length=50)
    slug = models.CharField(max_length=100)    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Catálogo de variacion'
        verbose_name_plural = 'Catálogo de variaciones'
        
    def __str__(self):
        return self.varcat
    
    
class Variation(models.Model):
    varcat = models.ForeignKey(VarCat, verbose_name='Catalogo variación', on_delete=models.PROTECT)
    variation = models.CharField('Variacion', max_length=50)
    slug = models.CharField(max_length=100)
    is_active = models.BooleanField('Activa', default=True)
    created_at = models.DateTimeField('Creada el', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Línea de variacion'
        verbose_name_plural = 'Línea de variaciones'

    def __str__(self):
        return self.variation


class Product(models.Model):
    name = models.CharField('Nombre prod', max_length=100, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    brand = models.CharField('Marca', max_length=50, blank=True)
    description = models.TextField('Descripción', max_length=300, blank=True)
    data_sheet = models.TextField('Ficha técnica', max_length=1000, blank=True)
    price = models.FloatField('Precio', blank=True)
    stock = models.IntegerField('Existencias totales', blank=True)
    stockvariations = models.ManyToManyField(Variation, through='StockVar', blank=True)
    tax = models.FloatField('Impuesto', blank=True,default=0.02)
    is_available = models.BooleanField('Disponible', default=True)

    has_discount = models.BooleanField('¿Descuento?', default=False)
    discount = models.FloatField(blank=True, null=True)
    low_price = models.FloatField('Precio con descuento', blank=True, default=0)
    start_by = models.DateTimeField(blank=True, null=True)
    end_by = models.DateTimeField(blank=True, null=True)

    image1 = models.ImageField(upload_to='photos/products', blank=True)
    image2 = models.ImageField(upload_to='photos/products', blank=True)
    image3 = models.ImageField(upload_to='photos/products', blank=True)
    image4 = models.ImageField(upload_to='photos/products', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(SubCategory, verbose_name='SubCategorias', blank=True)
    

    class Meta:
        verbose_name = 'producto'
        verbose_name_plural = 'productos'

    def get_url(self):
        subcat = None
        sub = self.categories.first()
        try:
            #subcat = SubCategory.objects.filter(id=self.id) No funciona para todos los casos
            subcat = SubCategory.objects.get(name=sub)
        except Exception as e:
            raise e
                                        # se deben regresar 2 slug: subcategory y product
        return reverse('product_detail', args=[subcat.slug, self.slug]) 
        # Sí funciona return reverse('product_detail', args=['pollo-engorda', self.slug])
        # No funciona return reverse('product_detail', args=[self.category.slug, self.slug])
    
    
    def __str__(self):
        return f"{self.name}"
    
    #Termina PRODUCT


class StockVar(models.Model):
    product = models.ForeignKey(Product, verbose_name='Producto', on_delete=models.CASCADE, blank=True, null=True)
    variation = models.ForeignKey(Variation, verbose_name='Variacion', on_delete=models.CASCADE, blank=True, null=True)
    value = models.CharField('Valor de la variacion',max_length=50)
    stock = models.IntegerField('Existencia por variación', blank=True, null=True)
    # No lleva diferente precio en variaciones: price = models.FloatField('Precio por variación', blank=True, default=None)
    
    class Meta:
        verbose_name = 'Existencia por variación'
        verbose_name_plural = 'Existencias por variación'
    
    
    def __str__(self):
        return f"{self.id} {self.variation.varcat} + {self.variation.variation} - {self.value}"

    # *****  OJO  *****
    # Todo sobre Many-to-Many relationships
    # https://docs.djangoproject.com/en/5.0/topics/db/examples/many_to_many/  
        
    # variation2 en lugar de value???
    #variation_2 = models.ForeignKey(Variation, verbose_name='Variacion 2',  related_name='variation2', on_delete=models.CASCADE, blank=True, null=True, default=Null)
    # https://stackoverflow.com/questions/543377/how-can-i-have-two-foreign-keys-to-the-same-model-in-django