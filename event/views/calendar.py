from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from event.forms import EventCreateForm
from event.models import Event


class CalendarView(LoginRequiredMixin, View):
    """ Calendar View. Main page """

    template_name = "calendar.html"
    form_class = EventCreateForm

    def get(self, request):
        form = self.form_class()
        events = Event.objects.get_all_events(user=request.user)
        events_month = Event.objects.get_running_events(user=request.user)
        event_list = []

        for event in events:
            event_list.append({
                "id": event.id,
                "title": event.title,
                "start": event.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                "end": event.end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                "description": event.description,
            })

        context = {
            "form": form,
            "events": event_list,
            "events_month": events_month
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
