"""
Cloud Module Models
"""
from django.db import models

from cloud.vaidators import PhoneValidator


class CloudyCustomer(models.Model):
    """Cloudy Customer Model"""
    phone = models.CharField(max_length=11, unique=True, validators=[PhoneValidator])
    fullName = models.CharField(max_length=255, blank=True)
    is_called = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)
    is_deployed = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    called_date = models.DateTimeField(null=True,blank=True)
    confirmed_date = models.DateTimeField(null=True,blank=True)
    deployed_date = models.DateTimeField(null=True,blank=True)
    cancelled_date = models.DateTimeField(null=True,blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    cafe = models.OneToOneField("cafe.Cafe", on_delete=models.DO_NOTHING, related_name="cloud")
    
    def __str__(self) -> str:
        return f"{self.fullName}-{self.phone}"