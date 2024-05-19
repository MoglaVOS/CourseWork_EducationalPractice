from django.shortcuts import redirect, render
from django.views.generic import View

from event.forms import ChatForm
from event.models.chat import ChatMessage


class ChatView(View):
    """ Message View """

    template_name = "chat.html"
    form_class = ChatForm

    def get(self, request, *args, **kwargs):
        # Show form
        form = self.form_class(user=request.user)
        context = {
            "message_count": ChatMessage.objects.get_message_count(),
            "messages": ChatMessage.objects.get_all_messages(),
            "form": form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # Create form
        form = ChatForm(request.POST, user=request.user)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.user = request.user
            msg.save()
            context = {
                "message_count": ChatMessage.objects.get_message_count(),
                "messages": ChatMessage.objects.get_all_messages(),
                "form": form
            }
            return render(request, self.template_name, context)