from django.urls import path
from . import views

app_name = "subscriptions"

urlpatterns = [
    path("subscribe/", views.subscribe, name="subscribe"),
    path("activate/", views.activate_subscription, name="activate"),
]
