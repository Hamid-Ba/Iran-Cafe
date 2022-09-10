"""
Cafe Module Views
"""
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiTypes
)
from rest_framework import (mixins , generics ,viewsets , permissions , authentication ,status)
from cafe.models import Cafe
from rest_framework.response import Response
from cafe.serializers import CafeSerializer, CreateUpdateCafeSerializer

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

@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'title',
                OpenApiTypes.STR,
                description= 'English Cafe Title'
            ),
            OpenApiParameter(
                'type',
                OpenApiTypes.STR,
                description= 'Cafe Type'
            ),
            OpenApiParameter(
                'city',
                OpenApiTypes.INT,
                description= 'Cafe City Id'
            )
        ]
    )
)
class CafesProvinceListView(generics.ListAPIView):
    serializer_class = CafeSerializer
        
    def get(self, request, province_slug):
        cafes = Cafe.objects.get_by_province(province_slug)
        
        try :
            if request.query_params['title'].strip() != "":
                cafes = cafes.filter(persian_title__contains=request.query_params['title'])
        except : None

        try :
            if request.query_params['city']:
                cafes = cafes.filter(city__id = request.query_params['city'])
        except : None

        try :
            if request.query_params['type']:
                cafes = cafes.filter(type = request.query_params['type'])
        except : None

        if len(cafes) == 0 : return Response(
            data ={"message" : "کافه ای برای این استان ثبت نشده است"},
            status = status.HTTP_204_NO_CONTENT)

        return Response(cafes) 

class CafesCityListView(generics.ListAPIView):
    serializer_class = CafeSerializer
        
    def get(self, request, city_slug):
        cafes = Cafe.objects.get_by_city(city_slug)
        
        if len(cafes) == 0 : return Response(
            data ={"message" : "کافه ای برای این شهر ثبت نشده است"},
            status = status.HTTP_204_NO_CONTENT)

        return Response(cafes) 