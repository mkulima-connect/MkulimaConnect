from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order
from products.models import Product
from django.http import JsonResponse
import uuid


@login_required
def place_order(request, pk):
    product = get_object_or_404(Product, id=pk)
    if request.method == "POST":
        quantity = max(1, int(request.POST.get("quantity", 1)))
        total_price = quantity * product.price
        external_id = f"ORDER-{uuid.uuid4().hex[:10]}"
        order = Order.objects.create(
            buyer=request.user,
            farmer=product.farmer,
            product=product,
            quantity=quantity,
            total_price=total_price,
            external_id=external_id,
            status="pending",
        )
        return redirect("orders:order_detail", order_id=order.id)
    return render(request, "orders/place_order.html", {"product": product})
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from .models import Order


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, buyer=request.user)
    return render(request, "orders/order_detail.html", {"order": order})
