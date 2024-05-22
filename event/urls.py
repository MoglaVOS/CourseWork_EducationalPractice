from django.urls import path

from event import views

app_name = "event"

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('chat/', views.ChatView.as_view(), name='chat'),
    path('eventchange/', views.EventChangeView.as_view(), name='eventchange'),
    path('notif_read/<int:notif_id>/', views.notif_read, name='notif_read'),
    path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
    path('next_week/<int:event_id>/', views.next_week, name='next_week'),
    path('next_day/<int:event_id>/', views.next_day, name='next_day'),
    path('next_date/<int:event_id>/', views.next_day, name='next_date'),
]
