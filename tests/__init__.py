from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class ModelTestMixin(TestCase):
    def create_user(self, username="user", role="buyer", password="pass12345"):
        return User.objects.create_user(username=username, password=password, role=role, email=f"{username}@example.com")
