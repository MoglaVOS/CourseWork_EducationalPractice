from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from account.forms import UserInviteForm


class UserInviteView(LoginRequiredMixin, View):
    """ User Invitation into calendar view """

    login_url = "account:signin"
    template_name = "invite.html"
    form_class = UserInviteForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {"form": form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, inviter=request.user)
        if form.is_valid():
            form = form.save(commit=False)
            form.inviter = request.user
            form.save()
            return redirect("event:dashboard")

        context = {"form": form}
        return render(request, self.template_name, context)
