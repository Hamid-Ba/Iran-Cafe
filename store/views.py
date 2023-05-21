from rest_framework import mixins
from rest_framework import status
from rest_framework import generics
from rest_framework import viewsets
from django.shortcuts import redirect
from rest_framework import permissions
from rest_framework import authentication
from rest_framework.response import Response
from django.contrib.sites.models import Site
from django.conf import settings
import requests

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

    def create(self, request, *args, **kwargs):
        user = self.request.user
        cafe_qs = Cafe.objects.filter(owner=user)
        request.data["user"] = user.id
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if cafe_qs.exists():
                serializer.save(cafe=cafe_qs.first())
            else:
                serializer.save()

            if settings.DEBUG:
                domain = Site.objects.filter(domain__contains="127").first()
                req_url = f"http://{domain}/api/payment/place_store_order/{serializer.data['id']}/"

            else:
                domain = Site.objects.filter(domain__contains="api.cafesiran").first()
                req_url = f"https://{domain}/api/payment/place_store_order/{serializer.data['id']}/"

            return redirect(req_url)
            # return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
