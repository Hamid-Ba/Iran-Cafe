"""
Plan Module Views 
"""
from rest_framework.response import Response
from rest_framework import (mixins , generics ,viewsets , permissions , authentication ,status ,views)
from plan.models import Plan

from plan.serializers import PlanSerializer

class PlanListView(generics.ListAPIView):
    """Plan List View"""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PlanSerializer
    queryset = Plan.objects.all()

    def get_queryset(self):
        return self.queryset.filter(is_active = True).order_by('-price')