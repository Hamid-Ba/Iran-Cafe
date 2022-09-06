"""
Test Cafe Module Models
"""
from django.test import TestCase
from django.template.defaultfilters import slugify
import uuid
from django.contrib.auth import get_user_model
from cafe.models import Cafe
from province.models import (Province , City)

def create_user(phone,password):
    """Helper Function for creating a user"""
    return get_user_model().objects.create_user(phone=phone,password=password)

def create_province(name,slug):
    """Helper Function To Create Province"""
    return Province.objects.create(name=name,slug=slug)

def create_city(name,slug,province):
    """Helper Function To Create Province"""
    return City.objects.create(name=name,slug=slug,province=province)

class CafeTest(TestCase):
    """Test Cafe Model"""
    def test_create_cafe_should_work_properly(self):
        """Test creating The Cafe Model"""
        payload = {
            # "code" : str(uuid.uuid1())[0:5],
            "persian_title" : "تست",
            "english_title" : "Test",
            "slug" : slugify("Test"),
            "phone" : "09151498722",
            "street" : "west coast street",
            "short_desc" : "test short desc",
            "desc" : "test description",
            "type" : "C"
        }
        owner = create_user("09151498722","123456")
        province = create_province("Tehran" , "Tehran")
        city = create_city("Tehran" , "Tehran", province)

        cafe = Cafe.objects.create(owner=owner,province=province,city=city,**payload)

        for (k , v) in payload.items():
            self.assertEqual(getattr(cafe,k),v)
        
        self.assertEqual(cafe.city , city)
        self.assertEqual(cafe.owner , owner)
        self.assertEqual(cafe.province , province)