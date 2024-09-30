from django.db import models


class ChatMessage(models.Model):
    sender = models.CharField(max_length=255)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}: {self.message} at {self.timestamp}"
