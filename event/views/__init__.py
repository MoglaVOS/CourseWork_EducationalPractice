from event.views.chat import ChatView
from .calendar import CalendarView, EventChangeView, notif_read
from .dashboard import DashboardView
from .calendar import (
    delete_event,
    copy_event
)

__all__ = [CalendarView, DashboardView, ChatView, delete_event, copy_event, notif_read]
