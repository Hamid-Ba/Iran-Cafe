"""
Test Plan Endpoints
"""
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from djmoney.money import Money
from django.contrib.auth import get_user_model
from cafe.models import Cafe
from plan.models import Plan
from plan.serializers import (PlanSerializer)

from province.models import City, Province

PLAN_URL = reverse('plan:plans')

def create_user(phone,password=None):
    """Helper Function For Create User"""
    return get_user_model().objects.create_user(phone=phone,password=password)

def create_plan(**new_payload):
    """Helper Function For Create Plan"""
    payload = {
            "title" : "Gold Plan",
            "period" : 31 ,
            "image" : "http://noImage.png",
            "price" : Money(25000,'IRR'),
            "desc" : "Gold Plan Description"
        }
    payload.update(**new_payload)
    return Plan.objects.create(**payload)

# class PublicTest(TestCase):
#     """Tests Which Does Not Need User To Be Authenticated"""
#     def setUp(self):
#         self.client = APIClient()

#     def test_return_unauthorized(self):
#         """Test if user is unauthorized"""
#         res = self.client.get(PLAN_URL)
#         self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)

class PrivateTest(TestCase):
    """Tests Which Need User To Be Authenticated"""
    def setUp(self):
        self.client = APIClient()
        self.user = create_user("09151498722" ,'123456')

        self.client.force_authenticate(self.user)

    def test_return_list_of_active_plans(self):
        """Test Return List Of Active Plans"""
        create_plan()
        create_plan()
        create_plan(**{"is_active" : False})

        res = self.client.get(PLAN_URL)
        self.assertEqual(res.status_code,status.HTTP_200_OK)

        plans = Plan.objects.filter(is_active=True).order_by('-price')
        serializer = PlanSerializer(plans,many = True)

        self.assertEqual(len(serializer.data) , len(res.data))