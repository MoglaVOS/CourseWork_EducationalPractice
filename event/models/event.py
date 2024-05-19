from datetime import datetime
from django.db import models

from account.models import User


class EventManager(models.Manager):
    """ Event manager """

    @staticmethod
    def get_all_events(user):
        """ Return all events for user """
        return Event.objects.filter(user=user, is_active=True, is_deleted=False)

    @staticmethod
    def get_running_events(user):
        """ Return running events for user """
        return Event.objects.filter(
            user=user,
            is_active=True,
            is_deleted=False,
            end_time__gte=datetime.now().date()
        ).order_by("start_time")


class Event(models.Model):
    """ Event model """

    PRIORITIES = (
        ("low", "Низкий"),
        ("medium", "Средний"),
        ("high", "Высокий"),
    )

    # Main Fields
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100, default='Место не определено')
    type = models.CharField(max_length=100, default='Тип не определен')
    priority = models.CharField(max_length=16, choices=PRIORITIES, default='low')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    # Static fields
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = EventManager()

    def __str__(self):
        return self.title
