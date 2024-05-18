from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash

from account.forms import ChangePasswordForm


class ChangePasswordView(View):
    """ Change Password Form """

    template_name = "change_password.html"
    form_class = ChangePasswordForm

    def get(self, request, *args, **kwargs):
        # Show form
        form = self.form_class()
        context = {"form": form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # Create form with current user data
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            # Save user and update session
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect("account:profile")
        context = {"form": form}
        return render(request, self.template_name, context)
