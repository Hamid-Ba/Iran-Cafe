"""
Cafe Module Views
"""
from datetime import datetime
from random import randint
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiTypes,
)

from django.contrib.auth import get_user_model
from rest_framework import (
    mixins,
    generics,
    viewsets,
    permissions,
    authentication,
    status,
    views,
)
from cafe.pagination import StandardPagination
from cafe.models import (
    Bartender,
    Cafe,
    Category,
    Customer,
    Gallery,
    MenuItem,
    Order,
    Reservation,
    Suggestion,
    Event,
    Branch,
    Table,
)
from rest_framework.response import Response
from cafe import serializers

from config.permissions import (
    AllowToFastRegister,
    HasCafe,
    UnauthenticatedCreatePermission,
)


class BaseMixinView(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """Base Mixin View Class"""

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)


class CafeViewSet(BaseMixinView):
    """Cafe View Set Class"""

    serializer_class = serializers.CafeSerializer
    queryset = Cafe.objects.all()

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    def get_serializer_class(self):
        """Specify The Serializer class"""
        if self.action == "create":
            self.serializer_class = serializers.CreateCafeSerializer

        if self.action == "update" or self.action == "partial_update":
            self.serializer_class = serializers.UpdateCafeSerializer

        return self.serializer_class

    def create(self, request, *args, **kwargs):
        is_bartender_exist = Bartender.objects.filter(
            user=self.request.user, is_active=True
        ).exists()
        if is_bartender_exist:
            return Response(
                {"message": "بارتندر عزیز ، شما قادر به ثبت کافه نمی باشید"},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        """Register Cafe"""
        return serializer.save(owner=self.request.user)


class CafeFastRegisterView(generics.CreateAPIView):
    """Cafe Fast Register View"""

    serializer_class = serializers.CreateCafeSerializer
    permission_classes = (AllowToFastRegister,)

    def perform_create(self, serializer):
        phone = self.request.data["phone"]
        otp = str(randint(100000, 999999))

        user, created = get_user_model().objects.get_or_create(phone=phone)
        user.set_password(otp)

        # For Test
        user.fullName = otp
        user.save()

        return serializer.save(owner=user)


class CafeDetailView(views.APIView):
    """Cafe Detail API View"""

    def get(self, request, cafe_id):
        cafe = Cafe.objects.get_valid_cafe_by_id(cafe_id=cafe_id)
        if not cafe:
            return Response(
                {"message": "کافه ای با این کد یافت نشد"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cafe.add_view()
        serializer = serializers.CafeSerializer(cafe)
        return Response(serializer.data)


class CafeIdView(views.APIView):
    """Cafe Id API View"""

    def get(self, request, cafe_code):
        cafe = Cafe.objects.get_valid_cafe_by_code(cafe_code=cafe_code)

        if cafe:
            return Response({"id": cafe.id}, status=status.HTTP_200_OK)

        return Response(
            {"message": "کافه ای با این کد یافت نشد"},
            status=status.HTTP_400_BAD_REQUEST,
        )


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                "title", OpenApiTypes.STR, description="English Cafe Title"
            ),
            OpenApiParameter("type", OpenApiTypes.STR, description="Cafe Type"),
            OpenApiParameter("city", OpenApiTypes.INT, description="Cafe City Id"),
        ]
    )
)
class CafesProvinceListView(generics.ListAPIView):
    serializer_class = serializers.CafeSerializer

    def get(self, request, province_slug):
        cafes = Cafe.objects.get_by_province(province_slug)

        try:
            if request.query_params["title"].strip() != "":
                cafes = cafes.filter(
                    persian_title__contains=request.query_params["title"]
                )
        except:
            None

        try:
            if request.query_params["city"]:
                cafes = cafes.filter(city__id=request.query_params["city"])
        except:
            None

        try:
            if request.query_params["type"]:
                cafes = cafes.filter(type=request.query_params["type"])
        except:
            None

        if len(cafes) == 0:
            return Response(
                data={"message": "کافه ای برای این استان ثبت نشده است"},
                status=status.HTTP_204_NO_CONTENT,
            )

        return Response(cafes)


class CafesCityListView(generics.ListAPIView):
    serializer_class = serializers.CafeSerializer

    def get(self, request, city_slug):
        cafes = Cafe.objects.get_by_city(city_slug)

        if len(cafes) == 0:
            return Response(
                data={"message": "کافه ای برای این شهر ثبت نشده است"},
                status=status.HTTP_204_NO_CONTENT,
            )

        return Response(cafes)


class CafesSearchView(views.APIView):
    """Cafes Search View Set.(Second Page)"""

    def get(self, request):
        cafes = Cafe.objects.all().order_by("-view_count").values()

        try:
            if request.query_params["code"].strip() != "":
                cafes = cafes.filter(code=request.query_params["code"]).first()
                return Response(cafes, status=status.HTTP_200_OK)
        except:
            None

        try:
            if request.query_params["title"].strip() != "":
                cafes = cafes.filter(
                    persian_title__contains=request.query_params["title"]
                )
        except:
            None

        try:
            if request.query_params["province"].strip() != "":
                cafes = cafes.filter(province__id=request.query_params["province"])
        except:
            None

        try:
            if request.query_params["city"]:
                cafes = cafes.filter(city__id=request.query_params["city"])
        except:
            None

        try:
            if request.query_params["type"]:
                cafes = cafes.filter(type=request.query_params["type"])
        except:
            None

        if len(cafes) == 0:
            return Response(
                data={"message": "کافه ای با این مشخصات یافت نشد"},
                status=status.HTTP_204_NO_CONTENT,
            )

        return Response(cafes, status=status.HTTP_200_OK)


class CategoryView(generics.ListAPIView):
    """Category List View."""

    serializer_class = serializers.CateogrySerializer
    queryset = Category.objects.filter(cafe=None)

    def get_queryset(self):
        return self.queryset.order_by("order")


class CategoryViewSet(mixins.ListModelMixin, mixins.DestroyModelMixin, BaseMixinView):
    """Category View Set."""

    serializer_class = serializers.CateogrySerializer
    permission_classes = (HasCafe,)
    queryset = Category.objects.all()

    def get_queryset(self):
        return self.queryset.filter(cafe__owner=self.request.user).order_by("order")

    def perform_create(self, serializer):
        return serializer.save(cafe=self.request.user.cafe)

    def perform_update(self, serializer):
        return serializer.save(cafe=self.request.user.cafe)


class CafeCategoryListView(generics.ListAPIView):
    """Cafe Category List View"""

    serializer_class = serializers.CateogrySerializer
    queryset = Category.objects.all()

    def get(self, request, cafe_id, *args, **kwargs):
        self.queryset = Category.objects.filter(cafe__id=cafe_id)
        self.queryset = self.queryset.order_by("order")
        return super().get(request, *args, **kwargs)


class MenuItemViewSet(mixins.ListModelMixin, mixins.DestroyModelMixin, BaseMixinView):
    serializer_class = serializers.MenuItemSerializer
    queryset = MenuItem.objects.all()
    pagination_class = StandardPagination

    def get_queryset(self):
        return self.queryset.filter(cafe__owner=self.request.user).order_by("-id")

    def get_serializer_class(self):
        """Specify The Serializer class"""
        if (
            self.action == "create"
            or self.action == "update"
            or self.action == "partial_update"
        ):
            self.serializer_class = serializers.CreateUpdateMenuItemSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        return serializer.save(cafe=self.request.user.cafe)


class MenuItemListView(generics.ListAPIView):
    serializer_class = serializers.MenuItemSerializer

    def get(self, request, cafe_id):
        menu_items = MenuItem.objects.get_active_items(cafe_id)

        if len(menu_items) == 0:
            return Response([])

        return Response(menu_items)


class GalleryViewSet(viewsets.ModelViewSet):
    """Gallery View Set"""

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.GallerySerializer
    queryset = Gallery.objects.all()
    pagination_class = StandardPagination

    def get_queryset(self):
        """Customize QuerySet"""
        return self.queryset.filter(cafe__owner=self.request.user)

    def get_serializer_class(self):
        """Specify The Serializer class"""
        if (
            self.action == "create"
            or self.action == "update"
            or self.action == "partial_update"
        ):
            self.serializer_class = serializers.CreateUpdateGallerySerializer

        return self.serializer_class

    def perform_create(self, serializer):
        return serializer.save(cafe=self.request.user.cafe)


class SuggestionView(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """Suggestion View"""

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.SuggestionSerializer
    queryset = Suggestion.objects.all()
    pagination_class = StandardPagination

    def get_queryset(self):
        cafe = Cafe.objects.filter(owner=self.request.user).exists()
        if cafe:
            return self.queryset.filter(cafe=self.request.user.cafe).order_by("-id")
        return []


class CreateSuggestionApiView(generics.CreateAPIView):
    """Create Suggestion API view"""

    serializer_class = serializers.SuggestionSerializer


class ReservationViewSet(
    mixins.ListModelMixin, mixins.DestroyModelMixin, BaseMixinView
):
    """Reservation View Set"""

    serializer_class = serializers.ReservationSerializer
    queryset = Reservation.objects.all()
    pagination_class = StandardPagination

    def get_queryset(self):
        is_cafe_exist = Cafe.objects.filter(owner=self.request.user).exists()
        if is_cafe_exist:
            return Reservation.objects.get_reservation(
                cafe=self.request.user.cafe, user=None
            ).order_by("-id")

        is_bartender_exist = Bartender.objects.filter(
            user=self.request.user, is_active=True
        ).exists()
        if is_bartender_exist:
            return Reservation.objects.get_reservation(
                cafe=None, user=None, bartender=self.request.user.bartender
            ).order_by("-id")

        return Reservation.objects.get_reservation(
            cafe=None, user=self.request.user
        ).order_by("-id")

    def get_serializer_class(self):
        """Specify The Serializer class"""
        if self.action == "create":
            self.serializer_class = serializers.CreateReservationSerializer

        if self.action == "update" or self.action == "partial_update":
            self.serializer_class = serializers.PatchReservationSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class OrderViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """Order ViewSet"""

    serializer_class = serializers.OrderSerializer
    queryset = Order.objects.all()
    pagination_class = StandardPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        state = "all"
        code = ""
        try:
            if self.request.query_params["state"].strip() != "":
                state = self.request.query_params["state"]
        except:
            None

        try:
            if self.request.query_params["code"].strip() != "":
                code = self.request.query_params["code"]
        except:
            None

        is_cafe_exist = Cafe.objects.filter(owner=self.request.user).exists()
        if is_cafe_exist:
            return Order.objects.get_order(
                state=state, code=code, cafe=self.request.user.cafe, user=None
            )

        is_bartender_exist = Bartender.objects.filter(
            user=self.request.user, is_active=True
        )
        if is_bartender_exist.exists():
            bartender = is_bartender_exist.first()
            return Order.objects.get_order(
                state=state, code=code, cafe=None, user=None, bartender=bartender
            )

        return Order.objects.get_order(
            state=state, code=code, cafe=None, user=self.request.user
        )

    def get_serializer_class(self):
        """Specify The Serializer class"""
        if self.action == "update" or self.action == "partial_update":
            self.serializer_class = serializers.PatchOrderSerializer

        return self.serializer_class

    def update(self, request, pk, *args, **kwargs):
        user = self.request.user

        if not Order.objects.filter(id=pk).exists():
            return Response(
                {"message": "سفارشی یافت نشد"}, status=status.HTTP_404_NOT_FOUND
            )

        order = Order.objects.filter(id=pk).first()

        if order.cafe.owner != user:
            return Response(
                {"message": "شما قادر به انجام این کار نیستید"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        state = request.data.get("state")

        if state:
            if state == "D":
                order.delivered()
                order.calc_total_price(datetime.now())
        return super().update(request, pk, *args, **kwargs)

    def partial_update(self, request, pk, *args, **kwargs):
        user = self.request.user

        if not Order.objects.filter(id=pk).exists():
            return Response(
                {"message": "سفارشی یافت نشد"}, status=status.HTTP_404_NOT_FOUND
            )

        order = Order.objects.filter(id=pk).first()

        if order.cafe.owner != user:
            return Response(
                {"message": "شما قادر به انجام این کار نیستید"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        state = request.data.get("state")

        if state:
            if state == "D":
                order.delivered()
                order.calc_total_price(datetime.now())
        return super().partial_update(request, pk, *args, **kwargs)

    def perform_update(self, serializer):
        return super().perform_update(serializer)


class PlaceOrderAPI(generics.CreateAPIView):
    serializer_class = serializers.CreateOrderSerializer
    queryset = Order.objects.all()

    def post(self, request, *args, **kwargs):
        """Create a New Order For Authenticated Normal User"""
        phone = request.data.get("phone")

        # Validate phone here (e.g., check if it's provided, is valid, etc.)
        if not phone:
            return Response(
                data={"message": "شماره موبایل خود را وارد نمایید"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user, created = get_user_model().objects.get_or_create(phone=phone)

        serializer = serializers.CreateOrderSerializer(data=request.data)
        if serializer.is_valid():
            if Cafe.objects.filter(owner=user).exists():
                return Response(
                    data={"message": "شما قادر به ثبت سفارش نمی باشید"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BartenderViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BartnederSerializer
    queryset = Bartender.objects.all()
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = StandardPagination

    def get_queryset(self):
        return self.queryset.filter(cafe__owner=self.request.user).order_by("-id")


class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CustomerSerializer
    queryset = Customer.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)
    pagination_class = StandardPagination
    http_method_names = ["get", "post", "head"]

    def get_queryset(self):
        is_cafe_exist = Cafe.objects.filter(owner=self.request.user).exists()
        if is_cafe_exist:
            return Customer.objects.filter(cafe=self.request.user.cafe).order_by("-id")
        return Customer.objects.filter(user=self.request.user).order_by("-id")

    def create(self, request, *args, **kwargs):
        serializer = serializers.CustomerSerializer(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            if Cafe.objects.filter(owner=self.request.user).exists():
                return Response(
                    data={"message": "شما نمیتوانید عضو شوید"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            elif Customer.objects.filter(
                user=self.request.user, cafe=request.data["cafe"]
            ).exists():
                return Response(
                    data={"message": "شما قبلا عضو باشگاه کاربران این کافه شده اید"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserClubsView(generics.ListAPIView):
    """User Clubs View"""

    queryset = Customer.objects.all()
    serializer_class = serializers.CustomerSerializer
    pagination_class = StandardPagination
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by("-id")


class EventModelViewSet(viewsets.ModelViewSet):
    """Event Model ViewSet"""

    queryset = Event.objects.filter(is_expired=False)
    permission_classes = (HasCafe,)
    serializer_class = serializers.EventSerializer
    pagination_class = StandardPagination
    authentication_classes = (authentication.TokenAuthentication,)

    def get_queryset(self):
        return Event.objects.filter(cafe=self.request.user.cafe).order_by(
            "-created_date"
        )

    def perform_create(self, serializer):
        return serializer.save(cafe=self.request.user.cafe)


class SingleEventView(generics.RetrieveAPIView):
    """Single Event View"""

    serializer_class = serializers.EventSerializer
    queryset = Event.objects.filter(status=True, is_expired=False)


class CafesEventView(generics.ListAPIView):
    """Cafes Event View"""

    serializer_class = serializers.CafeEventsSerializer
    queryset = Event.objects.filter(status=True, is_expired=False).order_by(
        "-created_date"
    )
    pagination_class = StandardPagination

    def get(self, request, cafe_id, *args, **kwargs):
        try:
            cafe = Cafe.objects.filter(pk=cafe_id).first()
        except Cafe.DoesNotExist:
            return Response({})

        try:
            if len(cafe.events.filter(status=True, is_expired=False)) == 0:
                return Response({})
        except:
            return Response({})

        serializer = self.serializer_class(instance=cafe)
        paginator = StandardPagination()
        res = paginator.paginate_queryset(serializer.data["events"], request)
        res = {"cafe": serializer.data["cafe"], "events": res}
        return Response(res)


class BranchViewSet(viewsets.ModelViewSet):
    """Branch View Set"""

    queryset = Branch.objects.all()
    permission_classes = (HasCafe,)
    serializer_class = serializers.BranchSerializer
    pagination_class = StandardPagination
    authentication_classes = (authentication.TokenAuthentication,)

    def get_queryset(self):
        return Branch.objects.filter(cafe=self.request.user.cafe).order_by("-id")

    def perform_create(self, serializer):
        return serializer.save(cafe=self.request.user.cafe)

    # def perform_destroy(self, instance):
    #     if instance.cafe != self.request.user.cafe:
    #         return Response("You do not have permission to perform this action.",status=status.HTTP_403_FORBIDDEN)
    #     return super().perform_destroy(instance)


class CafeBranchesApiView(generics.ListAPIView):
    """Cafe Branches"""

    serializer_class = serializers.CafeBranchesSerializer
    queryset = Branch.objects.filter(is_active=True).order_by("-id")
    pagination_class = StandardPagination

    def get(self, request, cafe_id, *args, **kwargs):
        try:
            cafe = Cafe.objects.filter(pk=cafe_id).first()
        except Cafe.DoesNotExist:
            return Response({})

        try:
            if len(cafe.branches.filter(is_active=True)) == 0:
                return Response({})
        except:
            return Response({})

        serializer = self.serializer_class(instance=cafe)
        paginator = StandardPagination()
        res = paginator.paginate_queryset(serializer.data["branches"], request)
        res = {"cafe": serializer.data["cafe"], "branches": res}
        return Response(res)


class SingleBranchView(generics.RetrieveAPIView):
    """Single Event View"""

    serializer_class = serializers.BranchSerializer
    queryset = Branch.objects.filter(is_active=True)


class TableViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = serializers.TableSerializer
    queryset = Table.objects.all()
    permission_classes = (HasCafe,)
    pagination_class = StandardPagination
    authentication_classes = (authentication.TokenAuthentication,)

    def get_queryset(self):
        return self.queryset.filter(cafe=self.request.user.cafe).order_by("-number")

    # def create(self, request, *args, **kwargs):
    #     number = self.request.data["number"]
    #     if Table.objects.filter(cafe=request.user.cafe, number=number).exists():
    #         return Response(
    #             {"message": "شما این میز را قبلا تعریف کرده اید"},
    #             status=status.HTTP_400_BAD_REQUEST,
    #         )

    #     return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        return serializer.save(cafe=self.request.user.cafe)


class DeleteTableAPIView(views.APIView):
    """Delete Table Api View"""

    permission_classes = (HasCafe,)
    authentication_classes = (authentication.TokenAuthentication,)

    def delete(self, request):
        cafe = request.user.cafe

        if cafe.tables_count() <= 0:
            return Response(
                {"message": "شما هیچ میزی ندارید"}, status=status.HTTP_400_BAD_REQUEST
            )

        last_table = cafe.last_table()

        last_table.delete()
        # last_table.save()

        return Response(
            {"message": "میز شما با موفقیت حذف گردید"},
            status=status.HTTP_204_NO_CONTENT,
        )
