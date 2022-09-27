"""
Plan Module Serializers
"""
from rest_framework.serializers import ModelSerializer

from plan.models import (Plan)

class PlanSerializer(ModelSerializer):
    """Plan Serializer"""
    class Meta:
        model = Plan
        fields = '__all__'