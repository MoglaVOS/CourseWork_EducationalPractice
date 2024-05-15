from django.shortcuts import redirect, render
from django.views.generic import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from event.forms import EventForm

from .models import Event

# Create your views here.

# TODO enable LoginRequiredMixin when accounts are done
class Calendar(View): 
    login_url = "accounts:signin"
    template_name = "calendar.html"
    form_class = EventForm
    
    def get(self, request):
        forms = self.form_class()
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
            "form": forms,
            "events": event_list,
            "events_month": events_month
        }
        return render(request, self.template_name, context)

    def post(self, request):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            form = forms.save(commit=False)
            form.user = request.user
            form.save()
            return redirect("calendarapp:calendar")
        
        context = {
            "form": forms
        }
        return render(request, self.template_name, context)
    
class Dashboard(TemplateView):
    template_name = 'dashboard.html'