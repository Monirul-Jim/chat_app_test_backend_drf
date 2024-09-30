from django.contrib import admin
from signup_login.models import ChatMessage, AddedUser
# Register your models here.
admin.site.register(ChatMessage)
admin.site.register(AddedUser)
