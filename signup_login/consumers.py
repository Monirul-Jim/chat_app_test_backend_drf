
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import ChatMessage


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'test'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

        self.send_existing_messages()

    def send_existing_messages(self):
        messages = ChatMessage.objects.all().order_by('timestamp')
        messages_data = [{'sender': msg.sender,
                          'message': msg.message,
                          'timestamp': msg.timestamp.isoformat()} for msg in messages]

        self.send(text_data=json.dumps({
            'type': 'history',
            'messages': messages_data
        }))

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json.get('sender', 'Anonymous')

        chat_message = ChatMessage.objects.create(
            sender=sender, message=message)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender,
                'timestamp': chat_message.timestamp.isoformat()
            }
        )

    def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        timestamp = event['timestamp']
        self.send(text_data=json.dumps({
            'type': 'chat',
            'sender': sender,
            'message': message,
            'timestamp': timestamp
        }))
