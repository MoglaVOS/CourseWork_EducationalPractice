from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from account.forms import SignInForm


class SignInView(View):
    """ User registration view """

    template_name = "signin.html"
    form_class = SignInForm

    def get(self, request, *args, **kwargs):
        forms = self.form_class()
        context = {"form": forms}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect("event:calendar")
            return redirect("account:signup")

        context = {"form": form}
        return render(request, self.template_name, context)
