from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'user', 'product', 'amount', 'currency', 'status', 'created_at')
    list_filter = ('status', 'currency', 'created_at')
    search_fields = ('transaction_id', 'user__username', 'product__name')
