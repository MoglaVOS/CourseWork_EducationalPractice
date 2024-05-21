from datetime import timedelta
from math import floor


def get_time_since(dt: timedelta):
    if dt.seconds == 0: return "только что"
    
    s = dt.total_seconds()
    
    interval = s / 31536000;
    if interval > 1: return f"{floor(interval)} лет";
    
    interval = s / 2592000;
    if interval > 1: return f"{floor(interval)} месяцев";
    
    interval = s / 86400;
    if interval > 1: return f"{floor(interval)} дней";
    
    interval = s / 3600;
    if interval > 1: return f"{floor(interval)} часов";
    
    interval = s / 60;
    if interval > 1: return f"{floor(interval)} минут";
    
    return f"{floor(dt.seconds)} секунд";