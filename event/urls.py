from django.urls import path

from event import views

app_name = "event"

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('chat/', views.ChatView.as_view(), name='chat'),
    path('event_change/<int:event_id>/', views.EventChangeView.as_view(), name='event_change'),
    path('notif_read/', views.notif_read, name='notif_read'),
    path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
    path('next_day/<int:event_id>/', views.next_day, name='next_day'),
    path('next_week/<int:event_id>/', views.next_week, name='next_week'),
    path('next_month/<int:event_id>/', views.next_month, name='next_month'),
    path('next_date/<int:event_id>/', views.next_day, name='next_date'),
]
