"""
Blog Module Views
"""
from rest_framework import (mixins,generics , permissions , authentication , viewsets ,status ,views)
from rest_framework.response import Response
from cafe.models import Cafe , Bartender
from blog import serializers , models
from django.utils import timezone 
from datetime import (timedelta,datetime)

class BaseMixinView(mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    """Base Mixin View Class"""
    authentication_classes = (authentication.TokenAuthentication ,)
    permission_classes = (permissions.IsAuthenticated ,)

class ManageBlogView(BaseMixinView):
    serializer_class = serializers.BlogSerializer
    # permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [authentication.TokenAuthentication]
    queryset = models.Blog.objects.all()

    def get_queryset(self):
        is_cafe = Cafe.objects.filter(owner=self.request.user).exists()
        if is_cafe :
            cafe = Cafe.objects.filter(owner=self.request.user).first()
            return self.queryset.filter(cafe_id=cafe.id).order_by('publish_date')

        is_bartender = Bartender.objects.filter(user=self.request.user,is_active=True).exists()
        if is_bartender:
            bartender = Bartender.objects.filter(user=self.request.user,is_active=True).first()
            return self.queryset.filter(cafe_id=bartender.cafe.id).order_by('publish_date')

    def get_serializer_class(self):
        if self.action == 'create' :
            self.serializer_class = serializers.CreateBlogSerializer
        
        if self.action == "update" or self.action == "partial_update":
            self.serializer_class = serializers.UpdateBlogSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        return serializer.save(user = self.request.user)

