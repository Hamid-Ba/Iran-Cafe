"""
Cafe Module Views
"""
from operator import ge
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiTypes
)
from rest_framework import (mixins , generics ,viewsets , permissions , authentication ,status ,views)
from cafe import serializers
from cafe.models import (Cafe,Category, Gallery, MenuItem, Order, Reservation, Suggestion)
from rest_framework.response import Response
from cafe.serializers import (CafeSerializer, CateogrySerializer, CreateOrderSerializer, CreateUpdateCafeSerializer,
 CreateUpdateGallerySerializer, CreateUpdateMenuItemSerializer, CreateUpdateReservationSerializer, GallerySerializer, MenuItemSerializer, OrderSerializer, PatchOrderSerializer
 , ReservationSerializer, SuggestionSerializer)

class BaseMixinView(mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    """Base Mixin View Class"""
    authentication_classes = (authentication.TokenAuthentication ,)
    permission_classes = (permissions.IsAuthenticated ,)

class CafeViewSet(BaseMixinView) :
    """Cafe View Set Class"""
    serializer_class = CafeSerializer
    queryset = Cafe.objects.all()

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    def get_serializer_class(self):
        """Specify The Serializer class"""
        if self.action == "create":
            self.serializer_class = CreateUpdateCafeSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Register Cafe"""
        return serializer.save(owner=self.request.user)

class CafeDetailView(views.APIView):
    """Cafe Detail API View"""
    def get(self, request, cafe_id):
        cafe = Cafe.objects.filter(id=cafe_id).first()
        if not cafe :
            return Response({"message" : "کافه ای با این کد یافت نشد"} , status = status.HTTP_400_BAD_REQUEST)
        
        serializer = CafeSerializer(cafe)
        return Response(serializer.data)

class CafeIdView(views.APIView):
    """Cafe Id API View"""
    def get(self, request,cafe_code):
        cafe = Cafe.objects.filter(code=cafe_code).first()

        if cafe : 
            return Response({"id" : cafe.id} , status = status.HTTP_200_OK)
        
        return Response({"message" : "کافه ای با این کد یافت نشد"} , status = status.HTTP_400_BAD_REQUEST)

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

class MenuItemViewSet(mixins.ListModelMixin,mixins.DestroyModelMixin,BaseMixinView) :
    serializer_class = MenuItemSerializer
    queryset = MenuItem.objects.all()

    def get_queryset(self):
        return self.queryset.filter(cafe__owner=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Specify The Serializer class"""
        if self.action == "create" or self.action == "update" or self.action == "partial_update":
            self.serializer_class = CreateUpdateMenuItemSerializer

        return self.serializer_class

    def perform_create(self,serializer):
        return serializer.save(cafe = self.request.user.cafe)

class MenuItemListView(generics.ListAPIView):
    serializer_class = MenuItemSerializer
    
    def get(self,request,cafe_id):        
        menu_items = MenuItem.objects.get_active_items(cafe_id)

        if len(menu_items) == 0 : return Response([])

        return Response(menu_items)

class GalleryViewSet(viewsets.ModelViewSet):
    """Gallery View Set"""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = GallerySerializer
    queryset = Gallery.objects.all()

    def get_queryset(self):
        """Customize QuerySet"""
        return self.queryset.filter(cafe__owner=self.request.user)

    def get_serializer_class(self):
        """Specify The Serializer class"""
        if self.action == "create" or self.action == "update" or self.action == "partial_update":
            self.serializer_class = CreateUpdateGallerySerializer

        return self.serializer_class

    def perform_create(self, serializer):
        return serializer.save(cafe = self.request.user.cafe)

class SuggestionView(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    """Suggestion View"""
    authentication_classes = (authentication.TokenAuthentication ,)
    permission_classes = (permissions.IsAuthenticated ,)
    serializer_class = SuggestionSerializer
    queryset = Suggestion.objects.all()
    
    def get_queryset(self):
        cafe = Cafe.objects.filter(owner=self.request.user).exists()
        if cafe :
            return self.queryset.filter(cafe =self.request.user.cafe).order_by('-id')
        return []
    
class CreateSuggestionApiView(generics.CreateAPIView):
    """Create Suggestion API view"""
    serializer_class = SuggestionSerializer

class ReservationViewSet(mixins.ListModelMixin,
                        mixins.DestroyModelMixin,
                        BaseMixinView):
    """Reservation View Set"""
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()

    def get_queryset(self):
        is_cafe_exist = Cafe.objects.filter(owner=self.request.user).exists()
        if is_cafe_exist:
            return Reservation.objects.get_reservation(cafe=self.request.user.cafe , user=None).order_by('-id')
        return Reservation.objects.get_reservation(cafe=None , user=self.request.user).order_by('-id')
    
    def get_serializer_class(self):
        """Specify The Serializer class"""
        if self.action == "create" or self.action == "update" or self.action == "partial_update":
            self.serializer_class = CreateUpdateReservationSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

class OrderViewSet(mixins.ListModelMixin,
                    BaseMixinView):
    """Order ViewSet"""
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        state = 'all'
        try :
            if self.request.query_params['state'].strip() != "":
                state = self.request.query_params['state']
        except : None

        is_cafe_exist = Cafe.objects.filter(owner=self.request.user).exists()
        if is_cafe_exist:
            return Order.objects.get_order(state=state,cafe=self.request.user.cafe , user=None)
        return Order.objects.get_order(state=state,cafe=None , user=self.request.user)

    def get_serializer_class(self):
        """Specify The Serializer class"""
        if self.action == "create" :
            self.serializer_class = CreateOrderSerializer
        
        if self.action == "update" or self.action == "partial_update":
            self.serializer_class = PatchOrderSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)