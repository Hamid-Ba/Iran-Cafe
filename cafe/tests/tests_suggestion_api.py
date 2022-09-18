"""
Test Suggestion Endpoints
"""
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from djmoney.money import Money
from cafe.models import (Cafe,Category, Suggestion)

from province.models import (City, Province)

SUGGESTION_URL = reverse('cafe:suggestion-list')
CREATE_SUGGESTION_URL = reverse('cafe:send_suggest')

def create_user(phone,password):
    """Helper Function for creating a user"""
    return get_user_model().objects.create_user(phone=phone,password=password)

def create_province(name,slug):
    """Helper Function To Create Province"""
    return Province.objects.create(name=name,slug=slug)

def create_city(name,slug,province):
    """Helper Function To Create Province"""
    return City.objects.create(name=name,slug=slug,province=province)

def create_cafe(province,city,owner,**new_payload):
    """Helper Function To Create Cafe"""
    payload  = {
        "persian_title" : "تست",
        "english_title" : "Test",
        "phone" : owner.phone,
        "street" : "west coast street",
        "desc" : "test description",
        "type" : "C",
        "state" : "C",
        "province" : province,
        "city" : city,
        "owner" : owner
    }
    payload.update(new_payload)
    return Cafe.objects.create(**payload)

class PublicTest(TestCase):
    """Test Cases Which Doesnt Need User To Be Authenticated"""
    def setUp(self):
        self.client = APIClient()
        self.province = create_province('Tehran','Tehran')
        self.city = create_city('Tehran','Tehran',self.province)
        self.owner = create_user('09151498722','123456')
        # self.cafe = create_cafe(self.province,self.city,self.owner)

    def test_send_suggest_for_cafe_should_work_properly(self):
        """Test Send Suggestion"""
        cafe = create_cafe(self.province,self.city,self.owner)
        payload = {
            'message' : 'test message',
            'cafe' : cafe.id
        }

        res = self.client.post(CREATE_SUGGESTION_URL,payload,format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        
        suggestion = Suggestion.objects.filter(cafe=cafe).exists()
        self.assertTrue(suggestion)