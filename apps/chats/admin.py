from django.contrib import admin

from apps.chats.models import Message, Dialog


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'dialog', 'text', 'is_read', 'created',)


@admin.register(Dialog)
class DialogAdmin(admin.ModelAdmin):
    pass
