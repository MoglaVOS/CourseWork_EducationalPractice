from datetime import timedelta
from django.shortcuts import redirect, render
from django.views.generic import View

from event.forms import ChatForm
from event.models.chat import ChatMessage
from event.models.notification import Notification


class ChatView(View):
    """ Message View """

    template_name = "chat.html"
    form_class = ChatForm

    def get(self, request, *args, **kwargs):
        # Show form
        form = self.form_class(user=request.user)
        
        notifications = Notification.objects.get_upcoming_notifications(user=request.user, time=timedelta(days=2))
        
        context = {
            "message_count": ChatMessage.objects.get_message_count(),
            "messages": ChatMessage.objects.get_all_messages(),
            "form": form,
            "notifications": notifications
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # Create form
        form = ChatForm(request.POST, user=request.user)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.user = request.user
            msg.save()
            return redirect("event:chat")