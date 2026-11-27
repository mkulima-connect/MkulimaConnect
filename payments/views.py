import json
import uuid

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator

from orders.models import Order
from .models import Transaction
from .services import PaymentGatewayService


def _sync_order_from_transaction(tx: Transaction):
    if not tx.order_id:
        return
    order = tx.order
    if tx.status == Transaction.STATUS_SUCCESS and order.status != Order.STATUS_PAID:
        order.status = Order.STATUS_PAID
        order.save(update_fields=["status", "updated_at"])
        product = order.product
        if product.quantity >= order.quantity:
            product.quantity -= order.quantity
        else:
            product.quantity = 0
        if product.quantity == 0:
            product.sold = True
        product.save(update_fields=["quantity", "sold", "updated_at"])
    elif tx.status in {Transaction.STATUS_FAILED, Transaction.STATUS_CANCELLED} and order.status == Order.STATUS_PENDING:
        order.status = Order.STATUS_CANCELLED
        order.save(update_fields=["status", "updated_at"])


@login_required
@require_POST
def initiate_payment(request, order_id):
    order = get_object_or_404(Order.objects.select_related("product"), id=order_id, buyer=request.user)
    if not order.is_payable:
        messages.error(request, "This order is not payable.")
        return redirect("orders:order_detail", order_id=order.id)

    account_number = request.POST.get("account_number", "").strip()
    provider = request.POST.get("provider", "azam").strip() or "azam"
    if not account_number:
        messages.error(request, "Account number is required.")
        return redirect("orders:order_detail", order_id=order.id)

    tx = Transaction.objects.create(
        user=request.user,
        order=order,
        product=order.product,
        amount=order.total_price,
        currency="TZS",
        transaction_id=f"TX-{uuid.uuid4().hex[:12].upper()}",
        status=Transaction.STATUS_PENDING,
    )
    response = PaymentGatewayService.send_payment(
        account_number=account_number,
        amount=tx.amount,
        currency=tx.currency,
        external_id=tx.transaction_id,
        provider=provider,
        additional_properties={"order_id": order.id, "product_id": order.product_id},
    )
    tx.raw_response = response
    tx.provider_reference = str(response.get("reference") or response.get("transactionId") or "")
    gateway_status = str(response.get("status", "")).lower()
    if response.get("ok") and gateway_status in {"success", "successful", "paid", "completed"}:
        tx.status = Transaction.STATUS_SUCCESS
    elif response.get("ok"):
        tx.status = Transaction.STATUS_PENDING
    else:
        tx.status = Transaction.STATUS_FAILED
    tx.save()
    _sync_order_from_transaction(tx)

    if tx.status == Transaction.STATUS_SUCCESS:
        messages.success(request, "Payment successful.")
    elif tx.status == Transaction.STATUS_PENDING:
        messages.info(request, "Payment initiated. Awaiting confirmation.")
    else:
        messages.error(request, response.get("message") or "Payment failed.")
    return redirect("orders:order_detail", order_id=order.id)


@method_decorator(csrf_exempt, name="dispatch")
class PaymentCallbackView(View):
    def post(self, request):
        try:
            payload = json.loads(request.body.decode("utf-8") or "{}")
        except (json.JSONDecodeError, UnicodeDecodeError):
            payload = request.POST.dict()
        tx_id = payload.get("externalId") or payload.get("transaction_id") or payload.get("external_id")
        status = str(payload.get("status", "")).lower()
        if not tx_id:
            return JsonResponse({"ok": False, "error": "missing transaction id"}, status=400)
        tx = Transaction.objects.filter(transaction_id=tx_id).first()
        if not tx:
            return JsonResponse({"ok": False, "error": "transaction not found"}, status=404)
        tx.raw_response = payload
        if status in {"success", "successful", "paid", "completed"}:
            tx.status = Transaction.STATUS_SUCCESS
        elif status in {"failed", "error"}:
            tx.status = Transaction.STATUS_FAILED
        elif status in {"cancelled", "canceled"}:
            tx.status = Transaction.STATUS_CANCELLED
        tx.save()
        _sync_order_from_transaction(tx)
        return JsonResponse({"ok": True, "status": tx.status})

    def get(self, request):
        return JsonResponse({"ok": True})


@login_required
def payment_list(request):
    txs = Transaction.objects.filter(user=request.user).select_related("order", "product")
    return render(request, "payments/payment_list.html", {"transactions": txs})
