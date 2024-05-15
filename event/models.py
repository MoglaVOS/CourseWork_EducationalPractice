from django.db import models
from django.urls import reverse

from datetime import datetime

# Create your models here.

class EventManager(models.Manager):
    """ Менеджер событий """

    # TODO fix when accounts are done
    def get_all_events(self, user):
        return Event.objects.filter(is_active=True, is_deleted=False) 
        #return Event.objects.filter(user=user, is_active=True, is_deleted=False)

    def get_running_events(self, user):
        running_events = Event.objects.filter(
            # TODO user=user,
            is_active=True,
            is_deleted=False,
            end_time__gte=datetime.now().date(),
        ).order_by("start_time")
        return running_events

class Event(models.Model):
    """ Модель события """

    # TODO when account app is done
    #user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100, default='место не определено')
    type = models.CharField(max_length=100, default='тип не определен')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = EventManager()
    
    def __str__(self):
        return self.title
