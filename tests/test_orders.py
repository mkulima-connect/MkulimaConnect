from decimal import Decimal
from django.urls import reverse
from orders.models import Order
from products.models import Product
from tests import ModelTestMixin


class OrderTests(ModelTestMixin):
    def setUp(self):
        self.farmer = self.create_user("farmer2", role="farmer")
        self.buyer = self.create_user("buyer2", role="buyer")
        self.product = Product.objects.create(
            farmer=self.farmer, name="Rice", description="Good", price=Decimal("1500.00"), location="Mbeya", quantity=5
        )

    def test_buyer_can_place_order(self):
        self.client.force_login(self.buyer)
        res = self.client.post(reverse("orders:place_order", args=[self.product.id]), {"quantity": 2})
        self.assertEqual(res.status_code, 302)
        order = Order.objects.get(buyer=self.buyer)
        self.assertEqual(order.quantity, 2)
        self.assertEqual(order.total_price, Decimal("3000.00"))

    def test_cannot_order_own_product(self):
        self.client.force_login(self.farmer)
        self.client.post(reverse("orders:place_order", args=[self.product.id]), {"quantity": 1}, follow=True)
        self.assertEqual(Order.objects.count(), 0)

    def test_cannot_order_more_than_stock(self):
        self.client.force_login(self.buyer)
        res = self.client.post(reverse("orders:place_order", args=[self.product.id]), {"quantity": 99}, follow=True)
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(res.status_code, 200)

    def test_order_detail_permissions(self):
        order = Order.objects.create(buyer=self.buyer, farmer=self.farmer, product=self.product, quantity=1, total_price=Decimal("1500.00"), external_id="ORD-1")
        other = self.create_user("other", role="buyer")
        self.client.force_login(other)
        res = self.client.get(reverse("orders:order_detail", args=[order.id]))
        self.assertEqual(res.status_code, 302)
