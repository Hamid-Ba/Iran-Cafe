"""
Test Order Endpoints
"""
from uuid import uuid4
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from djmoney.money import Money
from cafe.models import (Cafe,Category,MenuItem, Order)

from province.models import (City, Province)

ORDER_URL = reverse('cafe:order-list')

def order_detail_url(order_id):
    return reverse('cafe:order-detail', args=(order_id,))

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

def create_order(cafe,user,state):
    """Helper Function To Create Order"""
    payload = {
            "total_price" : 2000,
            "code" : str(uuid4())[:5],
            "state" : state,
            "items" : [
                {
                    "menu_item_id" : 1,
                    "title" : "test",
                    "image_url" : "https://imgae.jpg",
                    "desc" : "test description",
                    "price" : 1000,
                    "count" : 2
                }
            ]
        }
    
    order = Order.objects.create(cafe=cafe,user=user,
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

    return order

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
            "desc" : 'test description',
            "phone" : "09151498722",
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

    def test_cafe_owner_can_not_register_order(self):
        """Test That Cafe Owner Can Not Register Order"""
        self.client.force_authenticate(self.user)
        create_cafe(self.province,self.city,self.user)

        payload = {
            "total_price" :'20000',
            "desc" : 'test description',
            "phone" : "09151498720",
            "items" : [
                {
                    "menu_item_id" : 1,
                    "title" : 'test',
                    "image_url" : "https://noimage.png",
                    "desc" : "test description",
                    "price" : 10000,
                    "count" : 2
                },
            ],
            'cafe' : self.cafe.id
        }

        res = self.client.post(ORDER_URL,payload,format='json')
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

        self.assertTrue(Cafe.objects.filter(owner=self.user).exists())

    def test_change_order_state_should_work_properly(self):
        """Test Changing order state should work"""
        self.client.force_authenticate(self.owner)
        order = create_order(self.cafe,self.user,'P')
        payload = {
            'state' : 'D'
        }

        url = order_detail_url(order.id)
        res = self.client.patch(url, payload=payload,format='json')

        order.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_pendings_order(self):
        """Test Get Pending Orders"""
        self.client.force_authenticate(self.owner)
        create_order(self.cafe,self.user,'P')
        create_order(self.cafe,self.user,'D')
        create_order(self.cafe,self.user,'C')

        params = {"state":"P"}
        res = self.client.get(ORDER_URL,params)

        self.assertEqual(len(res.data['results']),1)

    def test_get_delivered_order(self):
        """Test Get Deliverd Orders"""
        self.client.force_authenticate(self.owner)
        create_order(self.cafe,self.user,'P')
        create_order(self.cafe,self.user,'D')
        create_order(self.cafe,self.user,'D')
        create_order(self.cafe,self.user,'D')
        create_order(self.cafe,self.user,'C')

        params = {"state":"D"}
        res = self.client.get(ORDER_URL,params)

        self.assertEqual(len(res.data['results']),3)

    def test_get_canceled_order(self):
        """Test Get Cancelled Orders"""
        self.client.force_authenticate(self.owner)
        create_order(self.cafe,self.user,'P')
        create_order(self.cafe,self.user,'D')
        create_order(self.cafe,self.user,'C')
        create_order(self.cafe,self.user,'C')

        params = {"state":"C"}
        res = self.client.get(ORDER_URL,params)

        self.assertEqual(len(res.data['results']),2)