from django.urls import reverse
from tests import ModelTestMixin


class ChatTests(ModelTestMixin):
    def test_chat_room_requires_login(self):
        res = self.client.get(reverse("chat:room", args=["testroom"]))
        self.assertEqual(res.status_code, 302)

    def test_chat_room_loads_for_authenticated_user(self):
        user = self.create_user("chatuser")
        self.client.force_login(user)
        res = self.client.get(reverse("chat:room", args=["testroom"]))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "testroom")
