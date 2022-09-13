"""
Test Cafe Module Models
"""
from django.test import TestCase
from django.template.defaultfilters import slugify
# from decimal import Decimal
from djmoney.money import Money

from django.contrib.auth import get_user_model
from cafe.models import (Cafe , Category, MenuItem)
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

def create_category(title):
    """Helper Function To Create Category"""
    return Category.objects.create(title=title)

def create_cafe(province,city,owner,**new_payload):
    """Helper Function To Create Cafe"""
    payload  = {
        "persian_title" : "تست",
        "english_title" : "Test",
        "slug" : slugify("Test"),
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

class CategoryTest(TestCase):
    """Test Category Model"""
    def test_create_category_should_work_properly(self):
        """Test creating The Category Model"""
        title = 'test category'
        image = 'test.jpg'

        category = Category.objects.create(title=title, image=image)

        self.assertEqual(category.title, title)
        self.assertEqual(category.image, image)

class MenuItemTest(TestCase):
    """Test Item Menu Model."""
    def setUp(self):
        self.province = create_province('Tehran','Tehran')
        self.city = create_city('Tehran','Tehran',self.province)
        self.owner = create_user('09151498722','123456')
        self.cafe = create_cafe(self.province,self.city,self.owner)
        self.category = create_category('Hot Baverage')

    def test_create_menu_item_should_work_properly(self):
        """Test Create Menu Item"""
        menu_item = {
            'image_url' : 'https://no_image.png',
            'title' : 'test title',
            'desc' : 'test description',
            'price' : Money(10,'IRR')
        }

        item = MenuItem.objects.create(category=self.category,cafe=self.cafe,**menu_item)

        for (key  ,value) in menu_item.items():
            self.assertEqual(getattr(item,key),value)
        
        self.assertEqual(item.cafe,self.cafe)
        self.assertEqual(item.category,self.category)