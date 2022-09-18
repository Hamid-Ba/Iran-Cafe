"""
Test Reservation Endpoints
"""
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from datetime import (date, datetime , time)

from cafe.models import (Cafe,Reservation)
from province.models import (City, Province)

RESERVATION_URL = reverse('cafe:reservation-list')

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
        res = self.client.get(RESERVATION_URL)
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)
    
    def test_post_unauthorized(self):
        """Test if user is unauthorized"""
        res = self.client.post(RESERVATION_URL)
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)

class PrivateTest(TestCase):
    """Tests Which Need User To Be Authenticated"""
    def setUp(self):
        self.client = APIClient()
        self.province = create_province("Tehran" , "Tehran")
        self.city = create_city("Tehran" , "Tehran",self.province)
        self.owner = create_user("09151498722",'123456')
        self.cafe = create_cafe(self.province,self.city,self.owner)
        self.user = create_user("09151498721",'123456')
        
    def test_book_reservation_should_work_properly(self):
        """Book reservation should work"""
        self.client.force_authenticate(self.user)

        payload = {
            "full_name" : "Afagh Balalzadeh",
            "phone" : self.user.phone,
            "date" : date(2023,2,5),
            "time" : time(17,35),
            "message" : "Hi I Want To Book a Table In This Date Time",
            "cafe" : self.cafe.id
        }

        res = self.client.post(RESERVATION_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)

        reserve = Reservation.objects.filter(user=self.user).order_by('-id')[0]

        for (key, value) in payload.items():
            if key == 'cafe' : self.assertEqual(reserve.cafe , self.cafe)
            else : self.assertEqual(getattr(reserve,key),value)

        self.assertEqual(reserve.user , self.user)