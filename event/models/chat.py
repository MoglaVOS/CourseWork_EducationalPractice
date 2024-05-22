from django.db import models

from account.models import User
from event.models.event import Event


class ChatMessageManager(models.Manager):
    """ Chat manager """

    @staticmethod
    def get_all_messages(event: Event | None = None):
        if event:
            return ChatMessage.objects.filter(is_deleted=False, event=event)
        return ChatMessage.objects.filter(is_deleted=False, event=None)

class ChatMessage(models.Model):
    """ Chat message model """

    # Main Fields
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    message = models.CharField(max_length=4000)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="messages", null=True, blank=True)

    # Static fields
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ChatMessageManager()

    def __str__(self):
        return self.message[:30]
