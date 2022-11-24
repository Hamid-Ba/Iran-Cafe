"""
Comment Module Views
"""
from django.shortcuts import render
from rest_framework import (mixins , generics ,viewsets , permissions , authentication ,status ,views)
from rest_framework.response import Response
from comment.models import Comment

from comment.serializers import CreateCommentSerializer

class BaseAuthView:
    """Base Mixin View Class"""
    permission_classes = (permissions.IsAuthenticated ,)
    authentication_classes = (authentication.TokenAuthentication ,)

# class CommentViewSet(viewsets.ViewSet):
#     """Create Comment View"""
#     permission_classes = (permissions.IsAuthenticated,)
#     authentication_classes = (authentication.TokenAuthentication ,)
    
#     def create(self, request):
#         # queryset = Comment.objects.all()
#         serializer = CreateCommentSerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)

#         return Response(serializer.errors)

class CreateCommentView(generics.CreateAPIView,BaseAuthView):
    """Create Comment View"""
    serializer_class = CreateCommentSerializer