from wsgiref.validate import validator
from rest_framework import serializers
from django.contrib.auth import get_user_model
from random import (randint)

class AuthenticationSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11,required=True)

    def create(self,validated_data):
        phone = validated_data.get('phone')
        otp = str(randint(100000,999999))
        
        user , created= get_user_model().objects.get_or_create(phone=phone)
        user.set_password(otp)
        user.save()

        return user