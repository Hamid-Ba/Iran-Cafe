"""
Account Module Views
"""
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken

from rest_framework.response import Response
from account.serializers import (AuthenticationSerializer , AuthTokenSerializer)
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

class AuthTokenView(ObtainAuthToken):
    """Auth Token View For Create Valid Token"""
    serializer_class = AuthTokenSerializer