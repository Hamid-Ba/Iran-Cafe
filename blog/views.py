"""
Blog Module Views
"""
from rest_framework import (generics , permissions , authentication ,status ,views)
from rest_framework.response import Response
from blog import serializers

class CreateBlogView(generics.CreateAPIView):
    serializer_class = serializers.CreateBlogSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def perform_create(self, serializer):
        return serializer.save(user = self.request.user)