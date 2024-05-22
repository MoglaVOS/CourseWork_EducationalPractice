from django.utils.timezone import localtime
from datetime import timedelta
from django.db import models

from account.models import User
from common.date import get_time_since
from event.models.event import Event


class NotificationManager(models.Manager):
    """ Event manager """

    @staticmethod
    def get_all_notifications(user):
        """ Return all notifications for user """
        return Notification.objects.filter(user=user, is_deleted=False)

    @staticmethod
    def get_unread_notifications(user):
        """ Return all unread notifications for user """
        return Notification.objects.filter(user=user, is_read=False, is_deleted=False)

    @staticmethod
    def get_upcoming_notifications(user, time: timedelta):
        """ Return or make all notifications for user about events
        that have less than `time` left to happen """
        print(localtime())
        upcoming = Event.objects.get_events_in(user=user, dt=time)
        notifications = []
        for event in upcoming:
            # Checking if user been issued a notification already
            notifs = Notification.objects.filter(
                user=user,
                event=event
            )[:1]
            if not notifs:
                # Making a notification
                notif = Notification.objects.create(
                    user=user,
                    title="Предстоящее событие",
                    description=f"Через {event.comes_in()} состоится \"{event.title}\"!",
                    event=event
                )
                notifications.append(notif)
            else:
                # Returning existing one if it is unread
                notif = notifs[0]
                if not notif.is_read:
                    notifications.append(notif)

        return notifications


class Notification(models.Model):
    """ Notification model """

    # Main Fields
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifs")
    title = models.CharField(max_length=200)
    description = models.TextField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="notifs")
    is_read = models.BooleanField(default=False)

    # Static fields
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = NotificationManager()

    def since(self):
        dt = localtime() - self.created_at
        if dt.seconds == 0: return "только что"
        return get_time_since(dt) + " назад"

    def __str__(self):
        return self.title
