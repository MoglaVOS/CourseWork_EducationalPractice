from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime, timedelta

from event.models import Event
from event.models.notification import Notification


class DashboardView(LoginRequiredMixin, View):
    """ Dashboard View. Table of events """

    login_url = "account:signin"
    template_name = 'dashboard.html'

    def get(self, request):
        today = datetime.today()

        events = Event.objects.get_all_events(user=request.user)
        current_events = Event.objects.get_events_by_date(user=request.user, date=today)
        upcoming_events = Event.objects.get_events_after_date(user=request.user, date=today + timedelta(days=1))
        notifications = Notification.objects.get_upcoming_notifications(user=request.user, time=timedelta(days=2))

        context = {
            "events": events,
            "current_events": current_events,
            "upcoming_events": upcoming_events,
            "notifications": notifications
        }
        return render(request, self.template_name, context)
