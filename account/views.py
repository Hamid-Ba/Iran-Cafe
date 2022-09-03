"""
Account Module Views
"""
from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status

from rest_framework.response import Response
from account.serializers import AuthenticationSerializer
# Create your views here.

class AuthenticationViewSet(viewsets.ViewSet):
    """Login & Register Viewset"""

    @action(detail=False,methods=['POST'])
    def login_or_register(self,request):
        """Login & Register Action"""
        serializer = AuthenticationSerializer(data= request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"phone" : serializer.data['phone'] } , status = status.HTTP_200_OK)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)