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
from cafe import serializers
from province.models import (City, Province)

CUSTOMER_URL = reverse('cafe:customer-list')
USER_CLUBS_URL = reverse('cafe:user_clubs')

def gallery_detail_url(gallery_id):
    return reverse('cafe:gallery-detail', args=(gallery_id,))

def create_customer(cafe,user,**new_payload):
    """Helper Function for creating a customer"""
    payload = {
        'phone' : user.phone,
        'firstName' : 'Hamid',
        'lastName' : 'Balalzadeh',
        'birthdate' : date.today()
    }
    payload.update(new_payload)
    return Customer.objects.create(user=user,cafe=cafe,**payload)

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

    def test_get_user_cafes_which_has_been_joined(self):
        """Test List Of Cafe Which has been joined"""
        user = create_user("09151498721",'123456')
        user_2 = create_user("09156789484",'123456')

        self.client.force_authenticate(user)
        owner2 = create_user("09151498723",'123456')
        cafe2 = create_cafe(self.province,self.city,owner2)

        club_1 = create_customer(self.cafe,user)
        club_2 = create_customer(cafe2,user)
        club_user_2 = create_customer(cafe2,user_2)

        res = self.client.get(USER_CLUBS_URL)           
        self.assertEqual(res.status_code,status.HTTP_200_OK)

        clubs = Customer.objects.filter(user=user).all().order_by('-id')
        serializer = serializers.CustomerSerializer(clubs,many=True)

        self.assertEqual(club_1.user , user)
        self.assertEqual(club_2.user , user)
        self.assertNotEqual(club_user_2.user,user)
        self.assertNotIn(club_user_2,serializer.data)
        self.assertEqual(res.data['results'] , serializer.data)