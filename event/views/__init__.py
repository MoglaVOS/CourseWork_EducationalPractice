from event.views.chat import ChatView
from .calendar import CalendarView, EventChangeView, notif_read
from .dashboard import DashboardView
from .calendar import (
    delete_event,
    next_week,
    next_day,
)

__all__ = [CalendarView, DashboardView, ChatView, delete_event, next_week, next_day, notif_read]
