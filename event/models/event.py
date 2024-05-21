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
    def get_events_by_date(user, date: datetime.date):
        """ Return events for user by date """
        return Event.objects.filter(
            user=user,
            is_active=True,
            is_deleted=False,
            start_time__date=date
        ).order_by("start_time")

    @staticmethod
    def get_events_after_date(user, date: datetime.date):
        """ Return events for user after date """
        return Event.objects.filter(
            user=user,
            is_active=True,
            is_deleted=False,
            start_time__gte=date
        ).order_by("start_time")


class Event(models.Model):
    """ Event model """

    PRIORITIES = (
        (0, "Низкий"),
        (1, "Средний"),
        (2, "Высокий"),
    )

    TYPE = (
        (0, "Тип не определен"),
        (1, "Личное"),
        (2, "Встреча"),
        (3, "Тренинг"),
        (4, "Конференция"),

    )

    # Main Fields
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100, default='Место не определено')
    type = models.IntegerField(choices=TYPE, default='none')
    priority = models.IntegerField(choices=PRIORITIES, default='low')
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
