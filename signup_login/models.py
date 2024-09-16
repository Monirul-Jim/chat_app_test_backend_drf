from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class ChatRoom(models.Model):
    name = models.CharField(max_length=100)
    participants = models.ManyToManyField(User, related_name="chat_rooms")

    def __str__(self):
        return self.name


class Message(models.Model):
    room = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    # File uploads
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    document = models.FileField(upload_to='documents/', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    audio = models.FileField(upload_to='audios/', blank=True, null=True)

    def __str__(self):
        return f'{self.sender.username}: {self.content[:20]}'
