"""
Account Module Models
"""
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser , PermissionsMixin , BaseUserManager)

from account.vaidators import phone_validator

class UserManager(BaseUserManager):
    """User Manager"""
    def create_user(self,phone,password,**extra_fields):
        """Custome Create Normal User"""
        user = self.model(phone=phone,**extra_fields)
        user.set_password(password)
        user.save()

        return user

class User(AbstractBaseUser,PermissionsMixin):
    """Custom User Model"""
    phone = models.CharField(max_length=11,unique=True,validators=[phone_validator])
    fullName = models.CharField(max_length=255,blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone'

    objects = UserManager()