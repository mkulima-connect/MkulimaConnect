from django.contrib import admin
from .models import Subscription

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'active', 'started_at', 'expires_at')
    list_filter = ('plan', 'active')
