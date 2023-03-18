from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import authentication

from config import permissions as custom_permission
from cafe.models import Cafe
from . import models
from . import serializers
from . import pagination

# Create your views here.


class ReturnMixinView(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    pagination_class = pagination.StandardPagination


class CategoryApiView(ReturnMixinView):
    """Category Api View"""

    queryset = models.StoreCategory.objects.all()
    serializer_class = serializers.CategorySerializer

    def get_queryset(self):
        return self.queryset.filter(sub_category=None).order_by("sortitem")


class ProductApiView(ReturnMixinView):
    """Product Api View"""

    queryset = models.Product.objects.order_by("-created_date")
    serializer_class = serializers.ProductSerializer


class StoreOrderApiView(mixins.CreateModelMixin, ReturnMixinView):
    """Order Api View"""

    queryset = models.StoreOrder.objects.all()
    serializer_class = serializers.StoreOrderSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user=user).order_by("-registered_date")

    def perform_create(self, serializer):
        user = self.request.user
        cafe_qs = Cafe.objects.filter(owner=user)

        if cafe_qs.exists():
            serializer.save(user=user, cafe=cafe_qs.first())
        else:
            serializer.save(user=user)

        return super().perform_create(serializer)
