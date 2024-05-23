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
    path('copy_event/<int:event_id>/', views.copy_event, name='copy_event'),
]
