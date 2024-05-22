from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime, timedelta
from django.http import JsonResponse, Http404

from event.forms import EventChangeForm, EventCreateForm
from event.models import Event
from event.models.notification import Notification
from account.models.invite import Invite
from account.models.user import User


class CalendarView(LoginRequiredMixin, View):
    """ Calendar View. Main page """
    model = Event
    login_url = "account:signin"
    template_name = "calendar.html"
    form_class = EventCreateForm

    def get(self, request):
        # Calendar owner. Inviter if provided else user
        inviter_id = request.GET.get("inviter_id")
        if inviter_id:
            try:
                owner = get_object_or_404(User, id=inviter_id)
                if not Invite.objects.filter(invitee_email=request.user.email, inviter=owner).exists():
                    new_request = request.GET.copy()
                    new_request.pop("inviter_id")
                    return redirect(reverse("event:calendar") + '?' + new_request.urlencode())
            except Http404:
                owner = request.user
        else:
            owner = request.user

        form = self.form_class()  # Create event form
        notifications = Notification.objects.get_all_notifications(user=request.user, time=timedelta(days=2))
        invites = Invite.objects.get_invites_by_invitee(request.user).filter(status=1)  # Other`s calendar tabs
        is_owner_in_overflow = True if owner in [x.inviter for x in invites[3:]] else False  # For dropdown menu
        events_today = Event.objects.get_events_by_date(user=owner, date=datetime.today())  # Side panel`s events
        event_list = [
            {
                "id": event.id,
                "title": event.title,
                "start": event.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                "end": event.end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                "location": event.location,
                "type": event.type,
                "priority": event.priority,
                "description": event.description,
            } for event in Event.objects.get_all_events(user=owner)
        ]  # Main calendar data

        context = {
            "form": form,
            "user": request.user,
            "owner": owner,
            "invites": invites,
            "is_owner_in_overflow": is_owner_in_overflow,
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


class EventChangeView(LoginRequiredMixin, View):
    """ Calendar View. Main page """
    model = Event
    login_url = "account:signin"
    template_name = "eventchange.html"
    form_class = EventChangeForm

    def get(self, request, event_id):
        ev = get_object_or_404(Event, id=event_id)
        
        form = self.form_class(instance=ev)  # Create event form

        context = {
            "form": form
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


def notif_read(request):
    if request.method == 'POST':
        notif_id = request.POST.get('notif_id')
        notif = get_object_or_404(Notification, id=notif_id)
        
        if request.user != notif.user:
            return JsonResponse({'message': 'Forbidden.'}, status=403)
        
        notif.is_read = True
        notif.save()
        return JsonResponse({'message': 'Complete.'})
    else:
        return JsonResponse({'message': 'Error!'}, status=400)


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


def next_date(request, event_id, time_delta_hours=0, time_delta_minutes=0, new_date=None, repetition_frequency=None):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        next_event = event
        next_event.id = None
        next_event.start_time += timedelta(days=1)
        next_event.end_time += timedelta(days=1)
        next_event.start_time += timedelta(hours=time_delta_hours, minutes=time_delta_minutes)
        next_event.end_time += timedelta(hours=time_delta_hours, minutes=time_delta_minutes)
        if new_date:
            next_event.start_date = new_date
            next_event.end_date = new_date
        if repetition_frequency == 'daily':
            next_event.start_time += timedelta(days=1)
            next_event.end_time += timedelta(days=1)
        elif repetition_frequency == 'weekly':
            next_event.start_time += timedelta(weeks=1)
            next_event.end_time += timedelta(weeks=1)
        elif repetition_frequency == 'monthly':
            next_event.start_time += timedelta(days=30)
            next_event.end_time += timedelta(days=30)
        next_event.save()
        return JsonResponse({'message': 'Успех!'})
    else:
        return JsonResponse({'message': 'Ошибка!'}, status=400)
