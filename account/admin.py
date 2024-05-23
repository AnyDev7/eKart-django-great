from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

# Register your models here.
class AccountAdmin(UserAdmin):

    list_display = ('email', 'username', 'is_active', 'first_name', 'last_name', 'last_login', 'joined_at')
    list_display_links = ('email', 'username')
    readonly_fields = ('last_login', 'joined_at')
    ordering = ('-joined_at',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)
