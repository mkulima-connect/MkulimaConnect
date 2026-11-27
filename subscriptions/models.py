from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone


class Subscription(models.Model):
    PLAN_BASIC = "basic"
    PLAN_PREMIUM = "premium"
    PLAN_CHOICES = [
        (PLAN_BASIC, "Basic"),
        (PLAN_PREMIUM, "Premium"),
    ]
    PLAN_DURATIONS = {
        PLAN_BASIC: timedelta(days=30),
        PLAN_PREMIUM: timedelta(days=30),
    }

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscriptions")
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default=PLAN_BASIC)
    active = models.BooleanField(default=True)
    started_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-started_at"]

    def __str__(self):
        return f"{self.user.username} - {self.plan}"

    @property
    def is_current(self):
        return self.active and (self.expires_at is None or self.expires_at >= timezone.now())

    def activate(self, plan=None):
        self.plan = plan or self.plan
        self.active = True
        self.started_at = timezone.now()
        self.expires_at = timezone.now() + self.PLAN_DURATIONS.get(self.plan, timedelta(days=30))
        self.save()
