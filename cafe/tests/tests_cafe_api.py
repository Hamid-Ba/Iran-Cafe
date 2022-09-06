"""
Test Cafe Endpoints
"""
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from django.template.defaultfilters import slugify
from django.contrib.auth import get_user_model
from cafe.models import Cafe

from province.models import City, Province

CAFE_URL = reverse('cafe:cafe-list')

def create_user(phone,password=None):
    """Helper Function For Create User"""
    return get_user_model().objects.create_user(phone=phone,password=password)

def create_province(name,slug):
    """Helper Function To Create Province"""
    return Province.objects.create(name=name,slug=slug)

def create_city(name,slug,province):
    """Helper Function To Create Province"""
    return City.objects.create(name=name,slug=slug,province=province)

class PrivateTest(TestCase):
    """Test Those Endpoints Which Need User To Be Authorized"""
    def setUp(self):
        self.client = APIClient()
        self.owner = create_user("09151498722")
        self.client.force_authenticate(self.owner)
    
    def test_register_cafe_should_work_properly(self):
        """Test Registering The Cafe By User"""
        province = create_province("Tehran" , "Tehran")
        city = create_city("Tehran" , "Tehran",province)
        payload = {
            # "code" : str(uuid.uuid1())[0:5],
            "persian_title" : "تست",
            "english_title" : "Test",
            "slug" : slugify("Test"),
            "phone" : "09151498722",
            "street" : "west coast street",
            "short_desc" : "test short desc",
            "desc" : "test description",
            "type" : "C",
            "province" : province.id,
            "city" : city.id
        }
        
        res = self.client.post(CAFE_URL, payload , format='json')

        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        self.assertTrue(Cafe.objects.filter(owner=self.owner).exists())