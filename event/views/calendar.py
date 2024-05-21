from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime, timedelta
from django.http import JsonResponse

from event.forms import EventCreateForm
from event.models import Event
from event.models.notification import Notification


class CalendarView(LoginRequiredMixin, View):
    """ Calendar View. Main page """
    model = Event
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


def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        event.delete()
        return JsonResponse({'message': 'Event success delete.'})
    else:
        return JsonResponse({'message': 'Error!'}, status=400)


def next_week(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        next_event = event
        next_event.id = None
        next_event.start_time += timedelta(days=7)
        next_event.end_time += timedelta(days=7)
        next_event.save()
        return JsonResponse({'message': 'Success!'})
    else:
        return JsonResponse({'message': 'Error!'}, status=400)


def next_day(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        next_event = event
        next_event.id = None
        next_event.start_time += timedelta(days=1)
        next_event.end_time += timedelta(days=1)
        next_event.save()
        return JsonResponse({'message': 'Sucess!'})
    else:
        return JsonResponse({'message': 'Error!'}, status=400)
