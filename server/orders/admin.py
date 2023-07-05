from django.contrib import admin
from .models import Order, OrderLine


class OrderLineInlineAdmin(admin.StackedInline):
    model = OrderLine


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('number', 'user', 'account', 'value', 'status', 'created_at')
    list_per_page = 12
    list_filter = ('status', 'created_at')
    inlines = [OrderLineInlineAdmin]
