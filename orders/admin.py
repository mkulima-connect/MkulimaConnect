from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'farmer', 'product', 'quantity', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('external_id', 'buyer__username', 'farmer__username', 'product__name')
