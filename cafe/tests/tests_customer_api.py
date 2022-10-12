"""
Test Customer Endpoints
"""
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from datetime import (date)
from django.contrib.auth import get_user_model

from cafe.models import (Cafe, Customer)
from province.models import (City, Province)

CUSTOMER_URL = reverse('cafe:customer-list')

def gallery_detail_url(gallery_id):
    return reverse('cafe:gallery-detail', args=(gallery_id,))

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
        "state" : "P",
        "province" : province,
        "city" : city,
        "owner" : owner
    }
    payload.update(new_payload)
    return Cafe.objects.create(**payload)

class PublicTest(TestCase):
    """Tests Which Does Not Need User To Be Authenticated"""
    def setUp(self):
        self.client = APIClient()
    
    def test_return_unauthorized(self):
        """Test if user is unauthorized"""
        res = self.client.get(CUSTOMER_URL)
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)

class PrivateTest(TestCase):
    """Tests Which Need User To Be Authenticated"""
    def setUp(self):
        self.client = APIClient()
        self.province = create_province("Tehran" , "Tehran")
        self.city = create_city("Tehran" , "Tehran",self.province)
        self.owner = create_user("09151498722",'123456')
        self.cafe = create_cafe(self.province,self.city,self.owner)
    
    def test_add_customer_should_work_properly(self):
        """Test Add Customer"""
        self.user = create_user("09151498721",'123456')
        self.client.force_authenticate(self.user)
        payload = {
            "cafe" : self.cafe.id,
            "firstName" : "Afagh",
            "lastName" : "Balalzadeh",
            "birthdate" : date(1996,2,2)
        }
        res = self.client.post(CUSTOMER_URL, payload)
        self.assertEqual(res.status_code , status.HTTP_201_CREATED)

        customer = Customer.objects.filter(user=self.user,cafe=self.cafe).first()

        for (key , value) in payload.items():
            if key == 'cafe' : continue
            self.assertEqual(getattr(customer,key), value)