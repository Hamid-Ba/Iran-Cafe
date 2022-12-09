"""
Blog Module Views
"""
from rest_framework import (mixins,generics , permissions , authentication , viewsets ,status ,views)
from rest_framework.response import Response
from blog.pagination import BlogPagination
from cafe.models import Cafe , Bartender
from blog import serializers , models
from django.utils import timezone 
from datetime import (timedelta,datetime)

class BaseMixinView(mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    """Base Mixin View Class"""
    authentication_classes = (authentication.TokenAuthentication ,)
    permission_classes = (permissions.IsAuthenticated ,)

class ManageBlogView(mixins.ListModelMixin,BaseMixinView):
    serializer_class = serializers.BlogSerializer
    # permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [authentication.TokenAuthentication]
    queryset = models.Blog.objects.all()

    def get_queryset(self):
        is_cafe = Cafe.objects.filter(owner=self.request.user).exists()
        if is_cafe :
            cafe = Cafe.objects.filter(owner=self.request.user).first()
            return self.queryset.filter(cafe_id=cafe.id).order_by('-publish_date')

        is_bartender = Bartender.objects.filter(user=self.request.user,is_active=True).exists()
        if is_bartender:
            bartender = Bartender.objects.filter(user=self.request.user,is_active=True).first()
            return self.queryset.filter(cafe_id=bartender.cafe.id).order_by('-publish_date')

    def get_serializer_class(self):
        if self.action == 'create' :
            self.serializer_class = serializers.CreateBlogSerializer
        
        if self.action == "update" or self.action == "partial_update":
            self.serializer_class = serializers.UpdateBlogSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        return serializer.save(user = self.request.user)

class CafesBlogListView(generics.ListAPIView):
    """List Of Cafes Blog View"""
    queryset = models.Blog.objects.all()
    serializer_class = serializers.BlogListSerializer
    pagination_class = BlogPagination

    def list(self, request, cafe_id):
        blogs = self.queryset.filter(cafe_id=cafe_id , publish_date__lte = timezone.now()).order_by('-publish_date')
        paginator = BlogPagination()
        result_page = paginator.paginate_queryset(blogs, request)
        serializer = serializers.BlogListSerializer(result_page,many=True)
        return Response({'data' : serializer.data} , status=status.HTTP_200_OK)

class BlogDetailView(views.APIView):
    """Detail Of Blog View"""
    def get(self, request,slug):
        try :
            blog = models.Blog.objects.filter(slug=slug , publish_date__lte = timezone.now()).first()
            serializer = serializers.BlogSerializer(blog)
            return Response({'data' : serializer.data} , status=status.HTTP_200_OK)
        except :
            return Response({'message' : 'مشکلی ایجاد شده'},status = status.HTTP_400_BAD_REQUEST)