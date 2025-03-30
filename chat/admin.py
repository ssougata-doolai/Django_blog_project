from django.contrib import admin
from . models import Chat

class ChatAdmin(admin.ModelAdmin):
    list_display = ['message','sender', 'receiver']

    class Meta:
        model = Chat

admin.site.register(Chat, ChatAdmin)
