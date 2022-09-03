"""
Account Module Serializers
"""
from rest_framework import serializers
from django.contrib.auth import (get_user_model , authenticate)
from random import (randint)

class AuthenticationSerializer(serializers.Serializer):
    """Authentcation Serializer For Login And Register"""
    phone = serializers.CharField(max_length=11,required=True)

    def validate(self, attrs):
        phone = attrs.get('phone')

        if not phone.isdigit() : return super().validate(attrs)

        return attrs

    def create(self,validated_data):
        """Login Or Register User"""
        phone = validated_data.get('phone')
        otp = str(randint(100000,999999))
        
        user , created= get_user_model().objects.get_or_create(phone=phone)
        user.set_password(otp)

        # For Test
        user.fullName = otp
        user.save()

        return user

class AuthTokenSerializer(serializers.Serializer):
    """Auth Token Serializer For Create Token"""
    phone = serializers.CharField(max_length=11,required=True,error_messages={'blank': 'موبایل خود را وارد نمایید'})
    password = serializers.CharField(max_length=11,required=True,error_messages={'blank': 'رمز یک بار مصرف خود را وارد نمایید'})

    def validate(self,attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')

        user = authenticate(
            request = self.context.get('request'),
            username = phone,
            password = password
        )

        if not user :
            msg = 'لطفا اطلاعات خود را درست وارد نمایید'
            raise serializers.ValidationError(msg,code='authorization')

        attrs['user'] = user
        return attrs