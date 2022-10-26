"""
Cafe Module Views
"""
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiTypes
)
from rest_framework import (mixins , generics ,viewsets , permissions , authentication ,status ,views)
from cafe.pagination import StandardPagination
from cafe.models import (Bartender, Cafe,Category, Customer, Gallery, MenuItem, Order, Reservation, Suggestion)
from rest_framework.response import Response
from cafe.serializers import (BartnederSerializer, CafeSerializer, CateogrySerializer, CreateOrderSerializer, CreateCafeSerializer, CustomerSerializer,UpdateCafeSerializer,
 CreateUpdateGallerySerializer, CreateUpdateMenuItemSerializer, CreateReservationSerializer, GallerySerializer, MenuItemSerializer, OrderSerializer, PatchOrderSerializer, PatchReservationSerializer
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
            self.serializer_class = CreateCafeSerializer

        if self.action == "update" or self.action == "partial_update":
            self.serializer_class = UpdateCafeSerializer

        return self.serializer_class

    def create(self, request, *args, **kwargs):
        is_bartender_exist = Bartender.objects.filter(user=self.request.user , is_active=True).exists()
        if is_bartender_exist:
            return Response({"message" : "بارتندر عزیز ، شما قادر به ثبت کافه نمی باشید"},status= status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        """Register Cafe"""
        return serializer.save(owner=self.request.user)

class CafeDetailView(views.APIView):
    """Cafe Detail API View"""
    def get(self, request, cafe_id):
        cafe = Cafe.objects.filter(id=cafe_id).first()
        if not cafe :
            return Response({"message" : "کافه ای با این کد یافت نشد"} , status = status.HTTP_400_BAD_REQUEST)
        
        cafe.add_view()
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

class CafesSearchView(views.APIView):
    """Cafes Search View Set.(Second Page)"""
    def get(self,request):
        cafes = Cafe.objects.all().order_by('-view_count').values()
       
        try :
            if request.query_params['code'].strip() != "":
                cafes = cafes.filter(code=request.query_params['code']).first()
                return Response(cafes,status= status.HTTP_200_OK) 
        except : None

        try :
            if request.query_params['title'].strip() != "":
                cafes = cafes.filter(persian_title__contains=request.query_params['title'])
        except : None
        
        try:
            if request.query_params['province'].strip() != "":
                cafes = cafes.filter(province__id=request.query_params['province'])
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
            data ={"message" : "کافه ای با این مشخصات یافت نشد"},
            status = status.HTTP_204_NO_CONTENT)

        return Response(cafes,status= status.HTTP_200_OK) 


class CategoryView(generics.ListAPIView):
    """Category List View."""
    serializer_class = CateogrySerializer
    queryset = Category.objects.all()

    def get_queryset(self):
        return self.queryset.order_by('-id')

class MenuItemViewSet(mixins.ListModelMixin,mixins.DestroyModelMixin,BaseMixinView) :
    serializer_class = MenuItemSerializer
    queryset = MenuItem.objects.all()
    pagination_class = StandardPagination

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
    pagination_class = StandardPagination

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
    pagination_class = StandardPagination
    
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
    pagination_class = StandardPagination

    def get_queryset(self):
        is_cafe_exist = Cafe.objects.filter(owner=self.request.user).exists()
        if is_cafe_exist:
            return Reservation.objects.get_reservation(cafe=self.request.user.cafe , user=None).order_by('-id')
        
        is_bartender_exist = Bartender.objects.filter(user=self.request.user,is_active=True).exists()
        if is_bartender_exist:
            return Reservation.objects.get_reservation(cafe=None,user=None,bartender=self.request.user.bartender).order_by('-id')

        return Reservation.objects.get_reservation(cafe=None , user=self.request.user).order_by('-id')
    
    def get_serializer_class(self):
        """Specify The Serializer class"""
        if self.action == "create":
            self.serializer_class = CreateReservationSerializer

        if self.action == "update" or self.action == "partial_update":
            self.serializer_class = PatchReservationSerializer
            
        return self.serializer_class

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

class OrderViewSet(mixins.ListModelMixin,
                    BaseMixinView):
    """Order ViewSet"""
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    pagination_class = StandardPagination

    def get_queryset(self):
        state = 'all'
        try :
            if self.request.query_params['state'].strip() != "":
                state = self.request.query_params['state']
        except : None

        is_cafe_exist = Cafe.objects.filter(owner=self.request.user).exists()
        if is_cafe_exist:
            return Order.objects.get_order(state=state,cafe=self.request.user.cafe , user=None)

        is_bartender_exist = Bartender.objects.filter(user=self.request.user , is_active=True)
        if is_bartender_exist.exists():
            bartender = is_bartender_exist.first()
            return Order.objects.get_order(state=state,cafe=None , user=None,bartender=bartender)

        return Order.objects.get_order(state=state,cafe=None , user=self.request.user)

    def get_serializer_class(self):
        """Specify The Serializer class"""
        if self.action == "create" :
            self.serializer_class = CreateOrderSerializer
        
        if self.action == "update" or self.action == "partial_update":
            self.serializer_class = PatchOrderSerializer

        return self.serializer_class

    def create(self, request, *args, **kwargs):
        """Create a New Order For Authenticated Normal User"""
        serializer = CreateOrderSerializer(data=request.data)
        if serializer.is_valid():
            if Cafe.objects.filter(owner=self.request.user).exists():    
                    return Response(data = {
                        "message" : "شما قادر به ثبت سفارش نمی باشید"
                    },status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save(user=self.request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class BartenderViewSet(viewsets.ModelViewSet):
    serializer_class = BartnederSerializer
    queryset = Bartender.objects.all()
    authentication_classes = (authentication.TokenAuthentication ,)
    permission_classes = (permissions.IsAuthenticated ,)
    pagination_class = StandardPagination

    def get_queryset(self):
        return self.queryset.filter(cafe__owner = self.request.user).order_by('-id')

class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    permission_classes = (permissions.IsAuthenticated ,)
    authentication_classes = (authentication.TokenAuthentication ,)
    pagination_class = StandardPagination
    http_method_names = ['get', 'post', 'head']
    
    def get_queryset(self):
        is_cafe_exist = Cafe.objects.filter(owner=self.request.user).exists()
        if is_cafe_exist:
            return Customer.objects.filter(cafe=self.request.user.cafe).order_by('-id')
        return Customer.objects.filter(user=self.request.user).order_by('-id')

    def create(self, request, *args, **kwargs):
        serializer = CustomerSerializer(data=request.data,context={'request' : request})

        if serializer.is_valid():
                if Cafe.objects.filter(owner=self.request.user).exists():    
                    return Response(data = {
                        "message" : "شما نمیتوانید عضو شوید"
                    },status=status.HTTP_400_BAD_REQUEST)
                    
                elif Customer.objects.filter(user=self.request.user,cafe=request.data['cafe']).exists() :
                    return Response(data = {
                        "message" : "شما قبلا عضو باشگاه کاربران این کافه شده اید"
                    },status=status.HTTP_400_BAD_REQUEST)

                serializer.save()
                return Response(serializer.data,status = status.HTTP_201_CREATED)

        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)