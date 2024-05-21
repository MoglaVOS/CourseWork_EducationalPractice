from django.db import models

from account.models import User


class ChatMessageManager(models.Manager):
    """ Chat manager """

    @staticmethod
    def get_all_messages():
        return ChatMessage.objects.filter(is_deleted=False)

    @staticmethod
    def get_message_count():
        return ChatMessage.objects.filter(is_deleted=False).count()

    @staticmethod
    def get_recent_messages():
        return ChatMessage.objects.filter(is_deleted=False).order_by("start_time")[:10]


class ChatMessage(models.Model):
    """ Chat message model """

    # Main Fields
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    message = models.CharField(max_length=4000)

    # Static fields
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ChatMessageManager()

    def __str__(self):
        return self.message[:30]
