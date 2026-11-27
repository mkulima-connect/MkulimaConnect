from django.urls import reverse
from django.contrib.auth import get_user_model
from tests import ModelTestMixin

User = get_user_model()


class AccountsTests(ModelTestMixin):
    def test_signup_creates_user(self):
        res = self.client.post(reverse("accounts:signup"), {
            "username": "newbuyer",
            "email": "newbuyer@example.com",
            "role": "buyer",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        })
        self.assertEqual(res.status_code, 302)
        self.assertTrue(User.objects.filter(username="newbuyer").exists())

    def test_profile_requires_login(self):
        res = self.client.get(reverse("accounts:profile"))
        self.assertEqual(res.status_code, 302)
        self.assertIn("/accounts/login/", res.url)
