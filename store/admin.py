from django.contrib import admin
from store.models import Product, VarCat, Variation, StockVar

# Register your models here.



class VarCatAdmin(admin.ModelAdmin):
    list_display = ('varcat', 'slug', 'created_at')
    prepopulated_fields = {
        'slug': ('varcat',)
    }
admin.site.register(VarCat, VarCatAdmin)

class VariationAdmin(admin.ModelAdmin):
    #inlines = ['StockVarInLine',]
    list_display = ('variation', 'created_at', 'varcat', 'is_active', 'slug', )
    search_fields = ('variation', )
    prepopulated_fields = {
        'slug': ('variation',)
    }
admin.site.register(Variation, VariationAdmin)


class StockVarInLine(admin.TabularInline):
    model = StockVar
    extra = 1
    autocomplete_fields = ['variation']
    #list_display = ('product', 'variation', 'stock')

# NO SE DEBE REGISTRAR StockVar que es la tabla ManyToMany    
#admin.site.register(StockVar, StockVarInLine)


class ProductAdmin(admin.ModelAdmin):
    inlines = [StockVarInLine,]
    list_display = ('name', 'stock', 'is_available', 'price', 'has_discount', 'low_price')
    list_editable = ('stock', 'is_available', 'price', 'has_discount', 'low_price')
    list_filter = ('is_available', 'has_discount', 'brand')
    prepopulated_fields = {
        'slug': ('name',)
    }
    filter_horizontal = ['categories', ] # checar que hace
admin.site.register(Product, ProductAdmin)