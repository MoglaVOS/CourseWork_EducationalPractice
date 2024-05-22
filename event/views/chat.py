from datetime import timedelta
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin


from event.forms import ChatForm
from event.models.chat import ChatMessage
from event.models.event import Event
from event.models.notification import Notification


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
        except Exception:
            ev = None
        
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
            except Exception:
                msg.event = None
                msg.save()
                return redirect("event:chat")
        
        context = {"form": form}
        return render(request, self.template_name, context)
