
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import ChatMessage
from django.utils import timezone


# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.room_group_name = 'test'
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#         )
#         self.accept()

#         self.send_existing_messages()

#     def send_existing_messages(self):
#         messages = ChatMessage.objects.all().order_by('timestamp')
#         messages_data = [{'sender': msg.sender,
#                           'message': msg.message,
#                           'timestamp': msg.timestamp.isoformat()} for msg in messages]

#         self.send(text_data=json.dumps({
#             'type': 'history',
#             'messages': messages_data
#         }))

#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#         sender = text_data_json.get('sender', 'Anonymous')

#         chat_message = ChatMessage.objects.create(
#             sender=sender, message=message)

#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message,
#                 'sender': sender,
#                 'timestamp': chat_message.timestamp.isoformat()
#             }
#         )

#     def chat_message(self, event):
#         message = event['message']
#         sender = event['sender']
#         timestamp = event['timestamp']
#         self.send(text_data=json.dumps({
#             'type': 'chat',
#             'sender': sender,
#             'message': message,
#             'timestamp': timestamp
#         }))

# this work for audio message

# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.room_group_name = 'test'
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#         )
#         self.accept()

#         self.send_existing_messages()

#     def send_existing_messages(self):
#         messages = ChatMessage.objects.all().order_by('timestamp')
#         messages_data = [{'sender': msg.sender,
#                           'message': msg.message,
#                           'timestamp': msg.timestamp.isoformat()} for msg in messages]

#         self.send(text_data=json.dumps({
#             'type': 'history',
#             'messages': messages_data
#         }))

#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#         sender = text_data_json.get('sender', 'Anonymous')

#         # Check if the message is an audio message (i.e., starts with 'data:audio/')
#         if message.startswith('data:audio/'):
#             # Store only the audio data in the database
#             chat_message = ChatMessage.objects.create(
#                 sender=sender, message=message)
#         else:
#             # Handle text messages
#             chat_message = ChatMessage.objects.create(
#                 sender=sender, message=message)

#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message,
#                 'sender': sender,
#                 'timestamp': chat_message.timestamp.isoformat()
#             }
#         )

#     def chat_message(self, event):
#         message = event['message']
#         sender = event['sender']
#         timestamp = event['timestamp']
#         self.send(text_data=json.dumps({
#             'type': 'chat',
#             'sender': sender,
#             'message': message,
#             'timestamp': timestamp
#         }))


# this work for sms audio voice and video call
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
        message = text_data_json.get('message', None)
        sender = text_data_json.get('sender', 'Anonymous')
        message_type = text_data_json.get('type', None)

        if message_type == "offer":
            self.handle_offer(sender, message)
        elif message_type == "answer":
            self.handle_answer(sender, message)
        elif message_type == "candidate":
            self.handle_candidate(sender, message)
        else:
            self.handle_chat_message(sender, message)

    def handle_offer(self, sender, offer):
        # Forward the offer to the group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'video_call_offer',
                'offer': offer,
                'sender': sender,
            }
        )

    def handle_answer(self, sender, answer):
        # Forward the answer to the group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'video_call_answer',
                'answer': answer,
                'sender': sender,
            }
        )

    def handle_candidate(self, sender, candidate):
        # Forward ICE candidate to the group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'video_call_candidate',
                'candidate': candidate,
                'sender': sender,
            }
        )

    def handle_chat_message(self, sender, message):
        # Handle text or audio messages
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

    def video_call_offer(self, event):
        self.send(text_data=json.dumps({
            'type': 'offer',
            'offer': event['offer'],
            'sender': event['sender']
        }))

    def video_call_answer(self, event):
        self.send(text_data=json.dumps({
            'type': 'answer',
            'answer': event['answer'],
            'sender': event['sender']
        }))

    def video_call_candidate(self, event):
        self.send(text_data=json.dumps({
            'type': 'candidate',
            'candidate': event['candidate'],
            'sender': event['sender']
        }))

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
