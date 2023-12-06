from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

from cafe.models import Cafe, Gallery, Category
from notifications import KavenegarSMS


@receiver(post_save, sender=Cafe, dispatch_uid="fille_unique_code")
def fill_cafe_unique_code(sender, instance, created, **kwargs):
    """Fill Cafe Unique Code After Confirmed"""
    if instance.state == "C":
        sender.objects.fill_unique_code(instance.id)

    if instance.state == "R" and not instance.code:
        kavenegar = KavenegarSMS()
        kavenegar.reject(instance.phone)
        kavenegar.send()


@receiver(post_delete, sender=Gallery)
def post_save_image(sender, instance, *args, **kwargs):
    """Clean Old Image file"""
    try:
        instance.image.delete(save=False)
    except:
        pass


@receiver(pre_save, sender=Gallery)
def pre_save_image(sender, instance, *args, **kwargs):
    """instance old image file will delete from os"""
    try:
        old_img = instance.__class__.objects.get(id=instance.id).image.path
        try:
            new_img = instance.image.path
        except:
            new_img = None
        if new_img != old_img:
            import os

            if os.path.exists(old_img):
                os.remove(old_img)
    except:
        pass
    
@receiver(post_delete, sender=Category)
def post_delete_category_image(sender, instance, *args, **kwargs):
    """Clean Old Image file"""
    try:
        instance.image.delete(save=False)
    except:
        pass
    
@receiver(pre_save, sender=Category)
def pre_save_image(sender, instance, *args, **kwargs):
    """instance old image file will delete from os"""
    try:
        old_img = instance.__class__.objects.get(id=instance.id).image.path
        try:
            new_img = instance.image.path
        except:
            new_img = None
        if new_img != old_img:
            import os

            if os.path.exists(old_img):
                os.remove(old_img)
    except:
        pass
