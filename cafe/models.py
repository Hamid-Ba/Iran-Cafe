"""
Cafe Module Models
"""
from django.db import models

from django.conf import settings
from cafe.validators import PhoneValidator
from province.models import (City, Province)

class Cafe(models.Model):
    """Cafe Model"""
    class CafeType(models.TextChoices):
        CAFE = 'C' , 'CAFE'
        RESTAURANT = 'R' , 'RESTAURANT',
        CAFE_RESTAURANT = 'CR' , 'CAFE_RESTAURANT'
    class CafeState(models.TextChoices):
        PENDING = 'P', 'Pending'
        CONFIRMED = 'C', 'Confirmed'
        REJECTED = 'R', 'Rejected'
    
    code = models.CharField(max_length=5,unique=True,null=True, blank=True)
    persian_title = models.CharField(max_length=85,null=False, blank=False)
    english_title = models.CharField(max_length=90,null=False, blank=False)
    slug = models.SlugField(max_length=200,blank=False,null=False)
    phone = models.CharField(max_length=11,unique=True,validators=[PhoneValidator])
    email = models.EmailField(max_length=125,null=False, blank=False)
    image_url = models.URLField(max_length=250)
    telegram_id = models.CharField(max_length=100)
    instagram_id = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    google_map_url = models.URLField(max_length=250)
    street = models.CharField(max_length=250,null=False, blank=False)
    short_desc = models.CharField(max_length=250,blank=False,null=False)
    desc = models.TextField(blank=True)
    state = models.CharField(max_length=1,
                            default=CafeState.PENDING,
                            choices=CafeState.choices)
    type = models.CharField(max_length=2,
                            default=CafeType.CAFE,
                            choices=CafeType.choices)
    
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    province = models.ForeignKey(Province, on_delete=models.DO_NOTHING)
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return self.persian_title