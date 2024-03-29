"""
site info module models
"""

from django.db import models
from datetime import timezone

from account.vaidators import phone_validator


class AboutUs(models.Model):
    """About Us Model"""

    text = models.TextField(blank=True, null=True)
    phones = models.CharField(max_length=60, null=True, blank=True)
    emails = models.CharField(max_length=175, null=True, blank=True)
    address = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "About Us"


class ContactUs(models.Model):
    """Contact Us Model"""

    full_name = models.CharField(max_length=125, blank=False, null=False)
    phone = models.CharField(
        max_length=11, blank=False, null=False, validators=[phone_validator]
    )
    message = models.TextField(blank=False, null=False)

    class Meta:
        verbose_name = "contactus"
        verbose_name_plural = "Contact Us"


class Robots(models.Model):
    """Robot Model"""

    name = models.CharField(max_length=50)
    text = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Robots"


class Error(models.Model):
    """Error Model"""

    time_raised = models.DateTimeField(auto_now_add=True, editable=False)
    reference = models.CharField(max_length=325)
    status = models.CharField(max_length=3, null=True, blank=True)
    description = models.TextField()

    def __str__(self) -> str:
        return f"{self.reference} - {self.time_raised}"
