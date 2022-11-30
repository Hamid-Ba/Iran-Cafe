"""
Comment Module Views
"""
from rest_framework import (mixins , generics ,viewsets , permissions , authentication ,status ,views)
from rest_framework.response import Response
from cafe.models import Bartender, Cafe

from comment.models import Comment
from comment.pagination import CommentPagination

from comment.serializers import CommentSerializer, CreateCommentSerializer, ResponseCommentSerializer

class BaseAuthView:
    """Base Mixin View Class"""
    permission_classes = (permissions.IsAuthenticated ,)
    authentication_classes = (authentication.TokenAuthentication ,)

class CreateCommentView(BaseAuthView,generics.CreateAPIView):
    """Create Comment View"""
    serializer_class = CreateCommentSerializer

class MenuItemCommentView(views.APIView):
    """Menu Item Comment View"""
    def get(self,request, item_id):
        try:
            comments = Comment.objects.filter(item_id=item_id,is_cafe=False).order_by('-date')
            if not comments : 
                return Response({'message' : 'کامنتی ثبت نشده است'} , status = status.HTTP_404_NOT_FOUND)
            serializer = CommentSerializer(comments,many=True)
            return Response({'data' : serializer.data},status=status.HTTP_200_OK)
        except :
            return Response({'message' : 'مشکلی ایجاد شده'},status = status.HTTP_400_BAD_REQUEST)

class SingleCommentView(BaseAuthView,views.APIView):
    """Single Comment View"""
    def get(self, request,id):
        try:
            comment = Comment.objects.filter(id=id).first()
            cafe = Cafe.objects.filter(id=comment.cafe_id).first()
            is_bartender = Bartender.objects.filter(cafe=cafe , user=request.user,is_active=True).exists()

            if cafe.owner == request.user or is_bartender:
                serializer = CommentSerializer(comment)
                return Response({'data' : serializer.data},status=status.HTTP_200_OK)
            
            return Response({'data' : 'به کامنت های دیگران دسترسی مجاز نیست'},status=status.HTTP_404_NOT_FOUND)
        except :
            return Response({'message' : 'مشکلی ایجاد شده'},status = status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id):
        try:
            comment = Comment.objects.filter(id=id).first()
            cafe = Cafe.objects.filter(id=comment.cafe_id).first()
            is_bartender = Bartender.objects.filter(cafe=cafe , user=request.user,is_active=True).exists()
    
            if cafe.owner == request.user or is_bartender:
                comment.delete()
                return Response({'data' : 'کامنت با موفقیت حذف شد'},status=status.HTTP_200_OK)
            
            return Response({'data' : 'به کامنت های دیگران دسترسی مجاز نیست'},status=status.HTTP_404_NOT_FOUND)
        except :
            return Response({'message' : 'مشکلی ایجاد شده'},status = status.HTTP_400_BAD_REQUEST)

class ResponseCommentView(BaseAuthView,generics.CreateAPIView):
    """Response Comment View"""
    serializer_class = ResponseCommentSerializer

class CafesCommentView(BaseAuthView,generics.ListAPIView):
    """Cafes Comment View"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = CommentPagination

    def get_queryset(self):
        user = self.request.user
        cafe = Cafe.objects.filter(owner=user)
        if cafe.exists() :
            return self.queryset.filter(cafe_id=cafe.first().id,is_cafe = False).order_by('-date')

        bartender = Bartender.objects.filter(user=user,is_active=True)
        if bartender.exists() :
            return self.queryset.filter(cafe_id=bartender.first().cafe.id,is_cafe = False).order_by('-date')

        return []

        