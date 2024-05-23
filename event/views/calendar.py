from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, Http404
from datetime import datetime, timedelta

from event.forms import EventForm
from event.models import Event
from event.models.notification import Notification
from account.models.invite import Invite
from account.models.user import User


class CalendarView(LoginRequiredMixin, View):
    """ Calendar View. Main page """
    model = Event
    login_url = "account:signin"
    template_name = "calendar.html"
    form_class = EventForm

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
        request.session["owner_id"] = owner.id  # Save owner_id for POST method

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
        # Get owner from session or user
        owner_id = request.session.get("owner_id") or request.user.id
        owner = User.objects.get(id=owner_id)

        # Create form
        form = self.form_class(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = owner
            form.save()

            if owner.id == request.user.id:
                return redirect("event:calendar")
            else:
                return redirect(reverse("event:calendar") + f"?inviter_id={owner.id}")

        context = {"form": form}
        return render(request, self.template_name, context)


class EventChangeView(LoginRequiredMixin, View):
    """ Calendar View. Main page """
    model = Event
    login_url = "account:signin"
    template_name = "event_change.html"
    form_class = EventForm

    def get(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        form = self.form_class(instance=event)  # Create event form

        # Handle permission
        members = [event.user] + [
            User.objects.get(email=x.invitee_email) for x in Invite.objects.get_invites_by_inviter(event.user)
        ]
        if request.user not in members:
            return redirect("event:calendar")

        context = {
            "form": form
        }
        return render(request, self.template_name, context)

    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        form = self.form_class(request.POST, instance=event)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = event.user
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


def copy_event(request, event_id):
    try:
        event = get_object_or_404(Event, id=event_id)
    except Http404:
        return JsonResponse({'message': 'Событие не существует'})
    days = int(request.POST.get("days"))

    if request.method == 'POST':
        new_event = event
        new_event.user = event.user
        new_event.id = None
        new_event.start_time += timedelta(days=days)
        new_event.end_time += timedelta(days=days)
        new_event.save()
        return JsonResponse({'message': 'Событие создано'})
    else:
        return JsonResponse({'message': 'Ошибка'}, status=400)
