from django.db import models
from django.conf import settings
from products.models import Product


class Subscription(models.Model):
    PLAN_CHOICES = [
        ('basic', 'Basic'),
        ('premium', 'Premium'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='basic')
    active = models.BooleanField(default=True)
    started_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.plan}"
