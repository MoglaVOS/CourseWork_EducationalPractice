from django.views.generic import View
from django.shortcuts import render, redirect

from account.forms import SignUpForm


class SignUpView(View):
    """ User registration view """

    template_name = "signup.html"
    form_class = SignUpForm

    def get(self, request, *args, **kwargs):
        forms = self.form_class()
        context = {"form": forms}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect("account:signin")
        context = {"form": forms}
        return render(request, self.template_name, context)
