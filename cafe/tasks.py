from celery import shared_task
from datetime import datetime, timedelta

from .models import Event


@shared_task
def event_cleaner():
    """Clean Event After One Week"""
    events = Event.objects.filter(is_expired=False)

    for event in events:
        event_time = datetime(
            event.created_date.year,
            event.created_date.month,
            event.created_date.day,
            event.created_date.hour,
            event.created_date.minute,
            event.created_date.second,
        )
        if event_time + timedelta(days=7) < datetime.now():
            event.is_expired = True
            event.save()
