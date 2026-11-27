import uuid
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from products.models import Product
from .models import Order


@login_required
@require_POST
def place_order(request, pk):
    product = get_object_or_404(Product, id=pk)
    if product.farmer_id == request.user.id:
        messages.error(request, "You cannot order your own product.")
        return redirect("products:product_detail", pk=pk)
    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        quantity = 1
    quantity = max(1, quantity)
    if quantity > product.quantity:
        messages.error(request, "Requested quantity exceeds available stock.")
        return redirect("products:product_detail", pk=pk)

    with transaction.atomic():
        product = Product.objects.select_for_update().get(id=pk)
        if quantity > product.quantity:
            messages.error(request, "Requested quantity exceeds available stock.")
            return redirect("products:product_detail", pk=pk)
        total_price = (product.price * Decimal(quantity)).quantize(Decimal("0.01"))
        order = Order.objects.create(
            buyer=request.user,
            farmer=product.farmer,
            product=product,
            quantity=quantity,
            total_price=total_price,
            external_id=f"ORDER-{uuid.uuid4().hex[:12].upper()}",
            status=Order.STATUS_PENDING,
        )
    messages.success(request, "Order placed. Proceed to payment.")
    return redirect("orders:order_detail", order_id=order.id)


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order.objects.select_related("product", "buyer", "farmer"), id=order_id)
    if request.user.id not in {order.buyer_id, order.farmer_id} and not request.user.is_staff:
        messages.error(request, "You do not have access to this order.")
        return redirect("products:product_list")
    return render(request, "orders/order_detail.html", {"order": order})


@login_required
def order_list(request):
    bought = Order.objects.filter(buyer=request.user).select_related("product", "farmer")
    sold = Order.objects.filter(farmer=request.user).select_related("product", "buyer")
    return render(request, "orders/order_list.html", {"bought_orders": bought, "sold_orders": sold})


@login_required
@require_POST
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, buyer=request.user)
    if order.status != Order.STATUS_PENDING:
        messages.error(request, "Only pending orders can be cancelled.")
        return redirect("orders:order_detail", order_id=order.id)
    order.status = Order.STATUS_CANCELLED
    order.save(update_fields=["status", "updated_at"])
    messages.success(request, "Order cancelled.")
    return redirect("orders:order_detail", order_id=order.id)
