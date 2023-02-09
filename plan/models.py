"""
Plan Module Models
"""
import os
from uuid import uuid4
from django.db import models
from djmoney.models.fields import MoneyField


def plan_image_file_path(instance, filename):
    """Generate file path for category image"""
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid4()}.{ext}"

    return os.path.join("uploads", "plans", filename)


class Plan(models.Model):
    """Plan Model"""

    title = models.CharField(max_length=80, blank=False, null=False)
    period = models.IntegerField(default=1, blank=False, null=False)
    price = MoneyField(
        max_digits=10, decimal_places=0, default_currency="IRR", null=False
    )
    image = models.ImageField(null=False, upload_to=plan_image_file_path)
    desc = models.TextField(blank=False, null=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
