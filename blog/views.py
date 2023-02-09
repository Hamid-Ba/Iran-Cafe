"""
Blog Module Views
"""
from rest_framework import (
    mixins,
    generics,
    permissions,
    authentication,
    viewsets,
    status,
    views,
)
from rest_framework.response import Response
from blog.pagination import BlogPagination
from cafe.models import Cafe, Bartender
from blog import serializers, models
from django.utils import timezone


class BaseMixinView(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """Base Mixin View Class"""

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)


class ManageBlogView(mixins.ListModelMixin, BaseMixinView):
    serializer_class = serializers.BlogSerializer
    # permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [authentication.TokenAuthentication]
    queryset = models.Blog.objects.all()

    def get_queryset(self):
        is_cafe = Cafe.objects.filter(owner=self.request.user).exists()
        if is_cafe:
            cafe = Cafe.objects.filter(owner=self.request.user).first()
            return self.queryset.filter(cafe_id=cafe.id).order_by("-publish_date")

        is_bartender = Bartender.objects.filter(
            user=self.request.user, is_active=True
        ).exists()
        if is_bartender:
            bartender = Bartender.objects.filter(
                user=self.request.user, is_active=True
            ).first()
            return self.queryset.filter(cafe_id=bartender.cafe.id).order_by(
                "-publish_date"
            )

    def get_serializer_class(self):
        if self.action == "create":
            self.serializer_class = serializers.CreateBlogSerializer

        if self.action == "update" or self.action == "partial_update":
            self.serializer_class = serializers.UpdateBlogSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class CafesBlogListView(generics.ListAPIView):
    """List Of Cafes Blog View"""

    queryset = models.Blog.objects.all()
    serializer_class = serializers.BlogListSerializer
    pagination_class = BlogPagination

    def get_queryset(self):
        cafe_code = self.kwargs["cafe_code"]
        cafe = Cafe.objects.filter(code=cafe_code).first()
        return self.queryset.filter(
            cafe_id=cafe.id, publish_date__lte=timezone.now()
        ).order_by("-publish_date")


class IranCafeBlogsView(generics.ListAPIView):
    """Iran Cafe Blogs View"""

    queryset = models.Blog.objects.all()
    serializer_class = serializers.BlogListSerializer
    pagination_class = BlogPagination

    def get_queryset(self):
        return self.queryset.filter(
            is_cafe=False, publish_date__lte=timezone.now()
        ).order_by("-publish_date")


class BlogDetailView(generics.RetrieveAPIView):
    """Detail Of Blog View"""

    lookup_field = "slug"
    queryset = models.Blog.objects.all()
    serializer_class = serializers.BlogSerializer


class BlogsView(generics.ListAPIView):
    """List Of Blogs View"""

    queryset = models.Blog.objects.all()
    pagination_class = BlogPagination
    serializer_class = serializers.BlogListSerializer

    def get_queryset(self):
        return self.queryset.filter(publish_date__lte=timezone.now()).order_by(
            "-publish_date"
        )


class LatestBlogsView(generics.ListAPIView):
    """List Of Latest Blogs View"""

    queryset = models.Blog.objects.all()
    serializer_class = serializers.LatestBlogSerializer

    def get_queryset(self):
        return self.queryset.filter(publish_date__lte=timezone.now()).order_by(
            "-publish_date"
        )[:3]
