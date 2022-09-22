"""
Test Order Endpoints
"""
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from djmoney.money import Money
from cafe.models import (Cafe,Category,MenuItem, Order)

from province.models import (City, Province)

ORDER_URL = reverse('cafe:order-list')

def create_user(phone,password):
    """Helper Function for creating a user"""
    return get_user_model().objects.create_user(phone=phone,password=password)

def create_province(name,slug):
    """Helper Function To Create Province"""
    return Province.objects.create(name=name,slug=slug)

def create_city(name,slug,province):
    """Helper Function To Create Province"""
    return City.objects.create(name=name,slug=slug,province=province)

def create_category(title):
    """Helper Function To Create Category"""
    return Category.objects.create(title=title)

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
        res = self.client.get(ORDER_URL)
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)
    
    def test_post_unauthorized(self):
        """Test if user is unauthorized"""
        res = self.client.post(ORDER_URL)
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)

class PrivateTest(TestCase):
    """Tests Which Need User To Be Authenticated"""
    def setUp(self):
        self.client = APIClient()
        self.province = create_province("Tehran" , "Tehran")
        self.city = create_city("Tehran" , "Tehran",self.province)
        self.owner = create_user("09151498722",'123456')
        self.user = create_user("09151498721",'123456')
        self.cafe = create_cafe(self.province,self.city,self.owner)
        self.category_1 = create_category('Hot Baverage')
        self.category_2 = create_category('Cold Liquid')
    
    def test_book_order_should_work_properly(self):
        """Test Book Order"""
        self.client.force_authenticate(self.user)
        menu_item = {
            'image_url' : 'https://no_image.png',
            'title' : 'test title',
            'desc' : 'test description',
            'price' : Money(10000,'IRR')
        }
        item_1 = MenuItem.objects.create(category=self.category_1,cafe=self.cafe,**menu_item)
        item_2 = MenuItem.objects.create(category=self.category_2,cafe=self.cafe,**menu_item)
        item_3 = MenuItem.objects.create(category=self.category_1,cafe=self.cafe,**menu_item)

        payload = {
            "total_price" :'30000',
            "items" : [
                {
                    "menu_item_id" : item_1.id,
                    "title" : item_1.title,
                    "image_url" : item_1.image_url,
                    "desc" : item_1.desc,
                    "price" : 10000,
                    "count" : 2
                },
                {
                    "menu_item_id" : item_2.id,
                    "title" : item_2.title,
                    "image_url" : item_2.image_url,
                    "desc" : item_2.desc,
                    "price" : 10000,
                    "count" : 1
                }
            ],
            'cafe' : self.cafe.id
        }
        res = self.client.post(ORDER_URL,payload,format='json')
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        
        order = Order.objects.all().order_by('-registered_date').first()

        self.assertEqual(order.items.count(),2)
        self.assertEqual(order.cafe , self.cafe)
        self.assertEqual(order.user , self.user)
        self.assertEqual(len(order.code),5)
        self.assertEqual(order.total_price , Money(30000,'IRR'))