import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import AnonymousUser

from .models import ChatRoom, Message


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        user = self.scope.get("user")
        if isinstance(user, AnonymousUser) or not user.is_authenticated:
            self.close()
            return
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        ChatRoom.objects.get_or_create(name=self.room_name)
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        if hasattr(self, "room_group_name"):
            async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)

    def receive(self, text_data=None, bytes_data=None):
        user = self.scope.get("user")
        if not user or not user.is_authenticated or not text_data:
            return
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            return
        message_content = (data.get("message") or "").strip()
        if not message_content:
            return
        chat_room, _ = ChatRoom.objects.get_or_create(name=self.room_name)
        new_message = Message.objects.create(chat_room=chat_room, sender=user, content=message_content[:2000])
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": new_message.content,
                "sender": user.username,
                "timestamp": new_message.timestamp.strftime("%H:%M"),
            },
        )

    def chat_message(self, event):
        self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"],
            "timestamp": event["timestamp"],
        }))
