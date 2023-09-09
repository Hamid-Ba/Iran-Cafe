from celery import shared_task
from datetime import datetime, timedelta

from .models import Event
from notifications import KavenegarSMS


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


@shared_task
def inform_manager_when_cafe_registered(cafe_id):
    """Send an SMS When a Cafe Get Registered"""
    kavenegar = KavenegarSMS()
    kavenegar.inform_registered_cafe(id=cafe_id)
    kavenegar.send()


@shared_task
def inform_manager_when_cafe_has_problem_to_receiving_sms(cafe_id):
    """Send an SMS When a Cafe Get Registered and has problem"""
    kavenegar = KavenegarSMS()
    kavenegar.problem_cafe_register(id=cafe_id)
    kavenegar.send()
