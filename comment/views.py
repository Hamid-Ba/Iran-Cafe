"""
Comment Module Views
"""
from rest_framework import (mixins , generics ,viewsets , permissions , authentication ,status ,views)
from rest_framework.response import Response
from cafe.models import Bartender, Cafe

from comment.models import Comment

from comment.serializers import CommentSerializer, CreateCommentSerializer

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
            comments = Comment.objects.filter(item_id=item_id).order_by('-date')
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
            is_bartender = Bartender.objects.filter(cafe=cafe , user=request.user).exists()
            print(is_bartender)

            if cafe.owner == request.user or is_bartender:
                serializer = CommentSerializer(comment)
                return Response({'data' : serializer.data},status=status.HTTP_200_OK)
            
            return Response({'data' : 'به کامنت های دیگران دسترسی مجاز نیست'},status=status.HTTP_404_NOT_FOUND)
        except :
            return Response({'message' : 'مشکلی ایجاد شده'},status = status.HTTP_400_BAD_REQUEST)
