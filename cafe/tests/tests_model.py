"""
Test Cafe Module Models
"""
from uuid import uuid4
from django.test import TestCase
# from decimal import Decimal
from djmoney.money import Money
from datetime import (datetime , time)
from django.contrib.auth import get_user_model
from cafe.models import (Cafe , Category, MenuItem , Gallery, Order, Suggestion , Reservation)
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

class GalleryTest(TestCase):
    """Test Gallery Model"""
    def setUp(self):
        self.province = create_province('Tehran','Tehran')
        self.city = create_city('Tehran','Tehran',self.province)
        self.owner = create_user('09151498722','123456')
        self.cafe = create_cafe(self.province,self.city,self.owner)

    def test_create_gallery_model_should_work_properly(self):
        """Test Create Gallery Model"""
        gallery = {
            "title" : "New Pic",
            "image" : "no_image.jpg"
        }

        created_gallery = Gallery.objects.create(cafe=self.cafe,**gallery)

        for (key, value) in gallery.items():
            self.assertEqual(getattr(created_gallery,key),value)

        self.assertEqual(created_gallery.cafe , self.cafe)

class SuggestionTest(TestCase):
    """Test Suggestion Model"""
    def setUp(self):
        self.province = create_province('Tehran','Tehran')
        self.city = create_city('Tehran','Tehran',self.province)
        self.owner = create_user('09151498722','123456')
        self.cafe = create_cafe(self.province,self.city,self.owner)

    def test_create_suggestion_model_should_work_properly(self):
        """Test Create Suggestion Model"""
        message = "Test Suggestion"

        suggest = Suggestion.objects.create(cafe = self.cafe, message = message)

        self.assertEqual(suggest.cafe , self.cafe)
        self.assertEqual(suggest.message , message)

class ReservationTest(TestCase):
    """Test Reservation Model"""
    def setUp(self):
        self.province = create_province('Tehran','Tehran')
        self.city = create_city('Tehran','Tehran',self.province)
        self.owner = create_user('09151498722','123456')
        self.cafe = create_cafe(self.province,self.city,self.owner)

    def test_create_reservation_model_should_work_properly(self):
        """Test Create Reservation Model"""
        client = create_user('09151498721','123456')
        payload = {
            "full_name" : "Afagh Balalzadeh",
            "phone" : client.phone,
            "date" : datetime(2022,6,20),
            "time" : time(17,35),
            "message" : "Hi I Want To Book a Table In This Date Time"
        }
        
        reserve = Reservation.objects.create(user=client,cafe = self.cafe, **payload)

        for (key  , value) in payload.items() :
            self.assertEqual(getattr(reserve,key),value)

        self.assertTrue(reserve.user)
        self.assertEqual(reserve.cafe , self.cafe)

class OrderTest(TestCase):
    """Test Order Model"""
    def setUp(self):
        self.province = create_province('Tehran','Tehran')
        self.city = create_city('Tehran','Tehran',self.province)
        self.owner = create_user('09151498722','123456')
        self.user = create_user('09151498721','123456')
        self.cafe = create_cafe(self.province,self.city,self.owner)

    def test_create_order_should_work_properly(self):
        """Test Create Order Model"""
        category_1 = create_category('Hot Baverage')
        category_2 = create_category('Cold Liquid')
        menu_item = {
            'image_url' : 'https://no_image.png',
            'title' : 'test title',
            'desc' : 'test description',
            'price' : Money(10,'IRR')
        }
        item_1 = MenuItem.objects.create(category=category_1,cafe=self.cafe,**menu_item)
        item_2 = MenuItem.objects.create(category=category_2,cafe=self.cafe,**menu_item)
        item_3 = MenuItem.objects.create(category=category_1,cafe=self.cafe,**menu_item)
        payload = {
            "total_price" : Money(910000,'IRR'),
            "code" : str(uuid4())[:5],
            "state" : 'P',
            "items" : [
                {
                    "menu_item_id" : item_1.id,
                    "title" : item_1.title,
                    "image_url" : item_1.image_url,
                    "desc" : item_1.desc,
                    "price" : item_1.price,
                    "count" : 2
                },
                {
                    "menu_item_id" : item_2.id,
                    "title" : item_2.title,
                    "image_url" : item_2.image_url,
                    "desc" : item_2.desc,
                    "price" : item_2.price,
                    "count" : 1
                }
            ]
        }

        order = Order.objects.create(cafe=self.cafe,user=self.user,
        total_price=payload['total_price'],code = payload['code'], state=payload['state'])

        for item in payload['items'] :
            # menu_item = MenuItem.objects.filter(id=item['id']).first()
            order.items.create(
                menu_item_id=item['menu_item_id'],
                title=item['title'],
                image_url=item['image_url'],
                desc =item['desc'],
                price=item['price'],
                count=item['count']
                )

        self.assertEqual(order.items.count(),2)
        self.assertEqual(order.user , self.user)
        self.assertEqual(order.cafe , self.cafe)