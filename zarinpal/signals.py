from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Payment


@receiver(post_save, sender=Payment, dispatch_uid="charge_cafe")
def charge_cafe(sender, instance, created, **kwargs):
    """Charge Cafe If Payment Was Successful"""
    if not created:
        if instance.is_payed:
            charge_days = instance.plan.period
            instance.cafe.charge_cafe(days=charge_days, is_first=False)
            instance.cafe.save()
