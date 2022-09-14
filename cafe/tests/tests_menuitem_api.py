"""
Test Menu Item Endpoints
"""
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from django.template.defaultfilters import slugify
from django.contrib.auth import get_user_model
from djmoney.money import Money
from cafe.models import (Cafe,Category,MenuItem)
from cafe.serializers import MenuItemSerializer

from province.models import (City, Province)

CREATE_MENU_ITEM_URL = reverse('cafe:menuitem-list')

def get_menu_item_url_by_slug(cafe_slug):
    """Returns The Menu Item By Cafe Slug"""
    return reverse('cafe:menuitem_list',kwargs={'cafe_slug': cafe_slug})

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
        "slug" : slugify(owner.phone),
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

def create_menu_item(cafe,category,**new_payload):
    payload = {
        'title' : 'test title',
        'image_url' : 'http://noImage.png',
        'desc' : 'test description',
        'price' : Money(10,'IRR'),
        'is_active' : True,
        'cafe' : cafe,
        'category' : category
    }
    payload.update(new_payload)
    return MenuItem.objects.create(**payload)

class PublicTest(TestCase):
    """Test Cases Which Doesnt Need User To Be Authenticated"""
    def setUp(self):
        self.client = APIClient()
        self.province = create_province('Tehran','Tehran')
        self.city = create_city('Tehran','Tehran',self.province)
        self.owner = create_user('09151498722','123456')
        self.cafe = create_cafe(self.province,self.city,self.owner)
        self.category = create_category('Hot Baverage')
    
    def test_return_list_of_cafe_menu_item_by_cafe_slug(self):
        """Test Retrieve Cafe Menu Items By Cafe Slug"""
        create_menu_item(self.cafe,self.category)
        create_menu_item(self.cafe,self.category)
        create_menu_item(self.cafe,self.category,**{'is_active' : False})
        
        new_owner = create_user("09151498721","123456")
        new_cafe = create_cafe(self.province,self.city,new_owner)
        create_menu_item(new_cafe,self.category)

        url = get_menu_item_url_by_slug(self.cafe.slug)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        menuitems = MenuItem.objects.filter(cafe_id=self.cafe.id).filter(is_active=True).order_by('-id').values()
        # serializer = MenuItemSerializer(menuitems,many=True)
        
        self.assertIn(menuitems[0],res.data)
        # self.assertEqual(res.data,serializer.data)
        self.assertEqual(len(res.data),2)

    def test_return_no_content_when_cafe_has_no_items(self):
        """Test Returns No Content When Cafe Has No Items"""
        new_owner = create_user("09151498721","123456")
        new_cafe = create_cafe(self.province,self.city,new_owner)

        url = get_menu_item_url_by_slug(new_cafe.slug)
        res = self.client.get(url)
        self.assertEqual(res.status_code,status.HTTP_204_NO_CONTENT)

        menuitems = MenuItem.objects.filter(cafe_id=new_cafe.id).filter(is_active=True).order_by('-id').values()

        self.assertEqual(len(menuitems),0)

class PrivateTest(TestCase):
    """Test Those Endpoints Which Don't Need User To Be Authorized"""
    def setUp(self):
        self.client = APIClient()
        self.province = create_province("Tehran" , "Tehran")
        self.city = create_city("Tehran" , "Tehran",self.province)
        self.owner = create_user("09151498722",'123456')
        self.cafe = create_cafe(self.province,self.city,self.owner)
        self.category = create_category('Hot Baverage')
        self.client.force_authenticate(self.owner)

    def test_create_menu_item_should_work_properly(self):
        """Test Create Menu Item should work correctly"""
        menu_item = {
            'image_url' : 'https://noimage.png',
            'title' : 'test title',
            'desc' : 'test description',
            'price': "068524949",
            'is_active' : True,
            'category' : self.category.id,
        }

        res = self.client.post(CREATE_MENU_ITEM_URL,menu_item,format = 'json')
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)

        item = MenuItem.objects.filter(cafe_id = self.cafe.id)[0]

        for (key  ,value) in menu_item.items():
            if key == 'category' : self.assertEqual(item.category.id,self.category.id)
            elif key == 'price' : self.assertEqual(getattr(item,key),Money(value,'IRR'))
            else : self.assertEqual(getattr(item,key),value)

        self.assertEqual(item.cafe , self.cafe)