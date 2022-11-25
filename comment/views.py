"""
Comment Module Views
"""
from django.shortcuts import render
from rest_framework import (mixins , generics ,viewsets , permissions , authentication ,status ,views)
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from comment.models import Comment

from comment.serializers import CommentSerializer, CreateCommentSerializer

class BaseAuthView:
    """Base Mixin View Class"""
    permission_classes = (permissions.IsAuthenticated ,)
    authentication_classes = (authentication.TokenAuthentication ,)

class CreateCommentView(generics.CreateAPIView,BaseAuthView):
    """Create Comment View"""
    serializer_class = CreateCommentSerializer

class MenuItemCommentView(views.APIView):
    def get(self,request, item_id):
        try:
            comments = Comment.objects.filter(item_id=item_id).order_by('-date')
            if not comments : 
                return Response({'message' : 'کامنتی ثبت نشده است'} , status = status.HTTP_404_NOT_FOUND)
            serializer = CommentSerializer(comments,many=True)
            return Response({'data' : serializer.data},status=status.HTTP_200_OK)
        except :
            return Response({'message' : 'مشکلی ایجاد شده'},status = status.HTTP_400_BAD_REQUEST)