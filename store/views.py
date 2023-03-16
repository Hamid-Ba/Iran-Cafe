from rest_framework import mixins , viewsets

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