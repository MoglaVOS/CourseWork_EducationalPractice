from django.urls import path

from event.views import Calendar, Dashboard

app_name = "event"

urlpatterns = [
    path('', Dashboard.as_view(), name='dashboard'),
    path('calendar', Calendar.as_view(), name='calendar')
]