from django.contrib import admin

from event.models.chat import ChatMessage
from event.models.event import Event
from event.models.notification import Notification


# Register your models here.

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ["title", "description", "user", "is_read", "is_deleted"]
    fields = ["user", "title", "description", "event", "created_at", "updated_at", "is_deleted"]
    readonly_fields = ["created_at", "updated_at"]
    search_fields = ["title", "description"]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["title", "description", "start_time", "end_time", "user", "is_active", "is_deleted"]
    fields = ["user", "title", "description", "location", "type", "priority", "start_time", "end_time", "is_active",
              "is_deleted"]
    readonly_fields = ["created_at", "updated_at"]
    search_fields = ["title", "description", "location"]


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ["message", "user", "event", "is_deleted"]
    fields = ["user", "message", "event", "is_deleted"]
    readonly_fields = ["created_at"]
    search_fields = ["message"]
