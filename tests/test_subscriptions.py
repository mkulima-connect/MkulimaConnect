from django.urls import reverse
from subscriptions.models import Subscription
from tests import ModelTestMixin


class SubscriptionTests(ModelTestMixin):
    def test_activate_subscription(self):
        user = self.create_user("subuser", role="buyer")
        self.client.force_login(user)
        res = self.client.post(reverse("subscriptions:activate"), {"plan": "premium"}, follow=True)
        self.assertEqual(res.status_code, 200)
        sub = Subscription.objects.get(user=user, active=True)
        self.assertEqual(sub.plan, "premium")
        self.assertTrue(sub.is_current)
