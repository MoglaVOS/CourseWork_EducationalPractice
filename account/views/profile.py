from django.views.generic import View
from django.shortcuts import render, redirect

from account.forms import SignUpForm


class ProfileView(View):
    template_name = "profile.html"
    form_class = SignUpForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {"form": form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect("account:signin")
        context = {"form": form}
        return render(request, self.template_name, context)
