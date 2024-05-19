from django.urls import path

from event import views

app_name = "event"

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('chat/', views.ChatView.as_view(), name='chat'),
]
