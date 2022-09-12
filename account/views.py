"""
Account Module Views
"""
from rest_framework import viewsets , generics ,permissions , authentication
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import logout


from rest_framework.response import Response
from account.serializers import (AuthenticationSerializer , AuthTokenSerializer, UserSerializer)

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

    @action(detail=False,methods=['POST'])
    def logout(self,request):
        """Logout Action"""
        try:
            request.user.auth_token.delete()
        except : pass
        logout(request)
        return Response('شما با موفقیت خارج شدید')

class AuthTokenView(ObtainAuthToken):
    """Auth Token View For Create Valid Token"""
    serializer_class = AuthTokenSerializer

class UserView(generics.RetrieveUpdateAPIView):
    """Retrieve Or Update APIView for User"""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        """Reterive The Authorized User"""
        return self.request.user