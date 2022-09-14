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
from cafe import serializers
from cafe.models import (Cafe,Category, MenuItem)
from rest_framework.response import Response
from cafe.serializers import CafeSerializer, CateogrySerializer, CreateUpdateCafeSerializer, MenuItemSerializer

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

class CategoryView(generics.ListAPIView):
    """Category List View."""
    serializer_class = CateogrySerializer
    queryset = Category.objects.all()

    def get_queryset(self):
        return self.queryset.order_by('-id')

class MenuItemView(generics.ListAPIView):
    serializer_class = MenuItemSerializer
    queryset = MenuItem.objects.all()
    
    def get(self,request,cafe_slug):        
        menu_items = MenuItem.objects.get_active_items(cafe_slug)
        serializer = MenuItemSerializer(menu_items,many=True)
        return Response(serializer.data)