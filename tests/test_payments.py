from decimal import Decimal
from django.urls import reverse
from orders.models import Order
from payments.models import Transaction
from products.models import Product
from tests import ModelTestMixin


class PaymentTests(ModelTestMixin):
    def setUp(self):
        self.farmer = self.create_user("farmer3", role="farmer")
        self.buyer = self.create_user("buyer3", role="buyer")
        self.product = Product.objects.create(
            farmer=self.farmer, name="Tomato", description="Red", price=Decimal("500.00"), location="Iringa", quantity=10
        )
        self.order = Order.objects.create(
            buyer=self.buyer, farmer=self.farmer, product=self.product, quantity=2, total_price=Decimal("1000.00"), external_id="ORD-PAY-1"
        )

    def test_payment_gateway_suspended(self):
        self.client.force_login(self.buyer)
        res = self.client.post(reverse("payments:initiate", args=[self.order.id]), {"provider": "manual", "account_number": "0712345678"}, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(Transaction.objects.count(), 0)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, Order.STATUS_PENDING)

    def test_callback_updates_transaction(self):
        tx = Transaction.objects.create(user=self.buyer, order=self.order, product=self.product, amount=self.order.total_price, transaction_id="TX-1")
        res = self.client.post(reverse("payments:callback"), data='{"externalId":"TX-1","status":"success"}', content_type="application/json")
        self.assertEqual(res.status_code, 200)
        tx.refresh_from_db()
        self.order.refresh_from_db()
        self.assertEqual(tx.status, Transaction.STATUS_SUCCESS)
        self.assertEqual(self.order.status, Order.STATUS_PAID)
