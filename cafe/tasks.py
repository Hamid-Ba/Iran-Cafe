from celery import shared_task
from datetime import datetime, timedelta

from .models import Event


@shared_task
def event_cleaner():
    """Clean Event After 6 Hours"""
    events = Event.objects.filter(is_expired=False)

    for event in events:
        event_time = datetime(
            event.date.year,
            event.date.month,
            event.date.day,
            event.time.hour,
            event.time.minute,
            event.time.second,
        )
        if event_time + timedelta(hours=6) < datetime.now():
            event.is_expired = True
            event.save()
