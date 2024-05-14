from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class Calendar(TemplateView):
    template_name = 'calendar.html'

class Dashboard(TemplateView):
    template_name = 'dashboard.html'