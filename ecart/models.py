from django.db import models
from store.models import Product, Variation, StockVar

# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'carrito'
        verbose_name_plural = 'carritos'

    def __str__(self):
        return self.cart_id
    
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    variations = models.ManyToManyField(StockVar, verbose_name="Variaciones", blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'producto en carrito'
        verbose_name_plural = 'productos en carritos'

    def sub_total(self):
        if not self.product.has_discount:
            return self.product.price * self.quantity
        else:
            return self.product.low_price * self.quantity

    def __unicode__(self):
        return self.product
    
    """
    def __str__(self):
        return str(self.product)
    """
