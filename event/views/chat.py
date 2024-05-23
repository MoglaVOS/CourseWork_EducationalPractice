from datetime import timedelta

from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin


from event.forms import ChatForm
from event.models.chat import ChatMessage
from event.models.event import Event
from event.models.notification import Notification
from account.models.user import User
from account.models.invite import Invite


class ChatView(LoginRequiredMixin, View):
    """ Message View """

    login_url = "account:signin"
    template_name = "chat.html"
    form_class = ChatForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(user=request.user)
        ev_id = request.GET.get("event")
        try:
            ev = get_object_or_404(Event, id=ev_id)
        except Http404:
            ev = None

        members = [ev.user] + [
            User.objects.get(email=x.invitee_email) for x in Invite.objects.get_invites_by_inviter(request.user)
        ]
        if request.user not in members:
            return redirect("event:calendar")

        notifications = Notification.objects.get_all_notifications(user=request.user, time=timedelta(days=2))
        
        context = {
            "event": ev,
            "messages": ChatMessage.objects.get_all_messages(event=ev),
            "form": form,
            "notifications": notifications
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # Create form
        form = self.form_class(request.POST, user=request.user)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.user = request.user
            try:
                msg.event = Event.objects.get(id=request.POST.get('event_id'))
                msg.save()
                return redirect(reverse("event:chat") + f"?event={msg.event.id}")
            except Event.DoesNotExist:
                msg.event = None
                msg.save()
                return redirect("event:chat")
        
        context = {"form": form}
        return render(request, self.template_name, context)
