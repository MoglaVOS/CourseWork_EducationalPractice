from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime, timedelta

from event.forms import EventCreateForm
from event.models import Event
from event.models.notification import Notification


class CalendarView(LoginRequiredMixin, View):
    """ Calendar View. Main page """

    login_url = "account:signin"
    template_name = "calendar.html"
    form_class = EventCreateForm

    def get(self, request):
        form = self.form_class()  # Create event form
        events_today = Event.objects.get_events_by_date(user=request.user, date=datetime.today())  # Side panel
        notifications = Notification.objects.get_upcoming_notifications(user=request.user, time=timedelta(days=2))
        event_list = []  # Calendar table

        # Fill calendar table
        for event in Event.objects.get_all_events(user=request.user):
            event_list.append({
                "id": event.id,
                "title": event.title,
                "start": event.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                "end": event.end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                "location": event.location,
                "type": event.type,
                "priority": event.priority,
                "description": event.description,
            })

        context = {
            "form": form,
            "events": event_list,
            "events_today": events_today,
            "notifications": notifications
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            return redirect("event:calendar")

        context = {"form": form}
        return render(request, self.template_name, context)
