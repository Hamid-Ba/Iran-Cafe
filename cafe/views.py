"""
Cafe Module Views
"""
import json
from typing import Generic
from rest_framework import (mixins , generics ,viewsets , permissions , authentication)
from cafe.models import Cafe
from rest_framework.views import APIView
from rest_framework.response import Response
from cafe.serializers import CafeSerializer, CreateUpdateCafeSerializer
from django.forms.models import model_to_dict

class CafeViewSet(mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet) :
    authentication_classes = (authentication.TokenAuthentication ,)
    permission_classes = (permissions.IsAuthenticated ,)
    serializer_class = CafeSerializer
    queryset = Cafe.objects.all()

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    def get_serializer_class(self):
        """Specify The Serializer class"""
        if self.action == "create" or self.action == "update":
            self.serializer_class = CreateUpdateCafeSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Register Cafe"""
        return serializer.save(owner=self.request.user)

class CafesListView(generics.ListAPIView):
    serializer_class = CafeSerializer
        
    def get(self, request, province_slug):
        cafes = Cafe.objects.get_by_province(province_slug)
        return Response(cafes) 