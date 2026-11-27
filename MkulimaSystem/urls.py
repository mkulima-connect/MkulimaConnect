from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("products/", include("products.urls")),
    path("orders/", include("orders.urls")),
    path("payments/", include("payments.urls")),
    path("chat/", include("chat.urls")),
    path("subscriptions/", include("subscriptions.urls")),
    path("", include("products.urls", namespace="products_home")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
