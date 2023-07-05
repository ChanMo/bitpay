from django.contrib import admin
from .models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('address', 'is_free', 'created_at')
    list_per_page = 12
    list_filter = ('is_free', 'created_at')
    exclude = ('private_key',)
