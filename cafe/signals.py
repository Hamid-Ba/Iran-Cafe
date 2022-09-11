from django.db.models.signals import (post_save)
from django.dispatch import receiver

from cafe.models import Cafe

@receiver(post_save ,sender = Cafe, dispatch_uid = 'fille_unique_code')
def fill_cafe_unique_code(sender, instance, created, **kwargs):
    """Fill Cafe Unique Code After Confirmed"""
    if instance.state == 'C':
        sender.objects.fill_unique_code(instance.id)