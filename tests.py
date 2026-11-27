from django.test import TestCase
from django.urls import reverse


class SmokeTests(TestCase):
    def test_homepage_loads(self):
        response = self.client.get('/')
        self.assertIn(response.status_code, [200, 302])

    def test_login_page_loads(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
