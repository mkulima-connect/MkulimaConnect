from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
    path("", views.payment_list, name="payment_list"),
    path("initiate/<int:order_id>/", views.initiate_payment, name="initiate"),
    path("callback/", views.PaymentCallbackView.as_view(), name="callback"),
]
