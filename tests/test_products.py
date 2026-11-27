from decimal import Decimal
from django.urls import reverse
from products.models import Product
from tests import ModelTestMixin


class ProductTests(ModelTestMixin):
    def setUp(self):
        self.farmer = self.create_user("farmer1", role="farmer")
        self.buyer = self.create_user("buyer1", role="buyer")
        self.product = Product.objects.create(
            farmer=self.farmer, name="Maize", description="Fresh", price=Decimal("1000.00"), location="Arusha", quantity=10
        )

    def test_product_list_and_detail(self):
        self.assertEqual(self.client.get(reverse("products:product_list")).status_code, 200)
        self.assertEqual(self.client.get(reverse("products:product_detail", args=[self.product.id])).status_code, 200)

    def test_farmer_can_create_product(self):
        self.client.force_login(self.farmer)
        res = self.client.post(reverse("products:product_create"), {
            "name": "Beans", "description": "Dry", "price": "2000", "location": "Moshi", "category": "grain", "quantity": 5
        })
        self.assertEqual(res.status_code, 302)
        self.assertTrue(Product.objects.filter(name="Beans").exists())

    def test_buyer_cannot_create_product(self):
        self.client.force_login(self.buyer)
        res = self.client.get(reverse("products:product_create"))
        self.assertEqual(res.status_code, 403)
