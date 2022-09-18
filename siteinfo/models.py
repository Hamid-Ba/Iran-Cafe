"""
site info module models
"""

from django.db import models

class AboutUs(models.Model):
    """About Us Model"""
    text = models.TextField(blank=True,null=True)
    phones = models.CharField(max_length=60,null=True,blank=True)
    emails = models.CharField(max_length=175,null=True,blank=True)
    address = models.TextField(blank=True,null=True)