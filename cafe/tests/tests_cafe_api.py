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
from cafe.serializers import CafeSerializer

from province.models import City, Province

CAFE_URL = reverse('cafe:cafe-list')

def get_cafe_province_url(slug):
    return reverse('cafe:cafes_by_province',kwargs={'province_slug': slug})

def get_cafe_city_url(slug):
    return reverse('cafe:cafes_by_city',kwargs={'city_slug': slug})

def create_user(phone,password=None):
    """Helper Function For Create User"""
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
        "slug" : slugify("Test"),
        "phone" : owner.phone,
        "street" : "west coast street",
        "short_desc" : "test short desc",
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
    """Test Those Endpoints Which Don't Need User To Be Authorized"""
    def setUp(self):
        self.client = APIClient()
        self.province = create_province("Tehran" , "Tehran")
        self.city = create_city("Tehran" , "Tehran",self.province)
        self.owner = create_user("09151498722")

    def test_get_cafes_by_province_should_work_properly(self):
        """Test Gets Cafe By Province"""
        payload = {
            "persian_title" : "تست",
            "english_title" : "Test",
            "slug" : slugify("Test"),
            "street" : "west coast street",
            "short_desc" : "test short desc",
            "desc" : "test description",
            "type" : "C",
            "state" : "C",
        }

        province_2 = create_province("NY" , "NY")
        city_2 = create_city("SD" , "SD",province_2)
        owner_2 = create_user("09151498721")
    
        create_cafe(self.province,self.city,self.owner,**payload)
        create_cafe(province_2,city_2,owner_2,**payload)

        url = get_cafe_province_url(self.province.slug)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        cafes = Cafe.objects.get_by_province(self.province.slug)
        self.assertEqual(len(cafes),1)
        self.assertTrue(cafes.exists())

    def test_get_empty_cafe_list_by_province(self):
        """Test If Provinces Cafe Are None"""
        url = get_cafe_province_url(self.province.slug)
        res = self.client.get(url)
        self.assertEqual(res.status_code,status.HTTP_204_NO_CONTENT)

    def test_get_cafes_list_if_cafe_confirmed(self):
        """Test If Cafe Is Confirmed Then Show It"""
        payload = {
            "persian_title" : "تست",
            "english_title" : "Test",
            "slug" : slugify("Test"),
            "phone" : "09151498722",
            "street" : "west coast street",
            "short_desc" : "test short desc",
            "desc" : "test description",
            "type" : "C",
            "state" : "C",
        }

        owner_2 = create_user("09151498721")
        create_cafe(self.province,self.city,self.owner,**payload)
        create_cafe(self.province,self.city,owner_2)
        
        url = get_cafe_province_url(self.province.slug)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        cafes = Cafe.objects.get_by_province(self.province.slug)
        self.assertEqual(len(cafes),1)
        self.assertTrue(cafes.exists())

    def test_filter_by_city_name_type(self):
        """Test Filter Cafes By City Name Type"""
        payload = {
            "persian_title" : "تست",
            "english_title" : "Test",
            "slug" : slugify("Test"),
            "phone" : "09151498722",
            "street" : "west coast street",
            "short_desc" : "test short desc",
            "desc" : "test description",
            "type" : "C",
            "state" : "C",
        }
        payload2 = {
            "persian_title" : "2تست",
            "english_title" : "Test2",
            "slug" : slugify("Test2"),
            "phone" : "09151498721",
            "street" : "west coast street",
            "short_desc" : "test short desc",
            "desc" : "test description",
            "type" : "R",
            "state" : "C",
        }
        payload3 = {
            "persian_title" : "3تست",
            "english_title" : "Test3",
            "slug" : slugify("Test3"),
            "phone" : "09151498723",
            "street" : "west coast street",
            "short_desc" : "test short desc",
            "desc" : "test description",
            "type" : "C",
            "state" : "C",
        }

        owner_2 = create_user("09151498721")
        city_2 = create_city("Shahriar" , "Shahriar",self.province)
        owner_3 = create_user("09151498723")
        c1 = create_cafe(self.province,self.city,self.owner,**payload)
        c2 = create_cafe(self.province,self.city,owner_2,**payload2)
        c3 = create_cafe(self.province,city_2,owner_3,**payload3)

        params = {"city":self.city.id , "title" : "تست" , "type" : "C"}
        url = get_cafe_province_url(self.province.slug)
        res = self.client.get(url,params)

        s1 = CafeSerializer(c1)
        s2 = CafeSerializer(c2)
        s3 = CafeSerializer(c3)
        
        self.assertEqual(len(res.data),1)
        self.assertEqual(s1.data['id'],res.data[0]['id'])
        self.assertNotEqual(s2.data['id'],res.data[0]['id'])
        self.assertNotEqual(s3.data['id'],res.data[0]['id'])
        

    def test_get_cafe_by_city_should_work_properly(self):
        """Test Get Cafe List Filterd By City"""
        payload = {
            "persian_title" : "تست",
            "english_title" : "Test",
            "slug" : slugify("Test"),
            "street" : "west coast street",
            "short_desc" : "test short desc",
            "desc" : "test description",
            "type" : "C",
            "state" : "C",
        }

        province_2 = create_province("NY" , "NY")
        city_2 = create_city("SD" , "SD",province_2)
        owner_2 = create_user("09151498721")

        create_cafe(self.province,self.city,self.owner,**payload)
        create_cafe(province_2,city_2,owner_2)

        url = get_cafe_city_url(self.city.slug)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        cafes = Cafe.objects.get_by_city(self.city.slug)
        self.assertEqual(len(cafes) , 1)
        self.assertTrue(cafes.exists())

    def test_get_empty_cafe_list_by_city(self):
        """Test Get None Cafe If No Cafe Registered In City"""
        url = get_cafe_city_url(self.city.slug)
        res = self.client.get(url)
        self.assertEqual(res.status_code,status.HTTP_204_NO_CONTENT)

    def test_get_cafe_list_by_city_if_cafe_confirmed(self):
        """Test Get Confirmed Cafes"""
        payload = {
            "persian_title" : "تست",
            "english_title" : "Test",
            "slug" : slugify("Test"),
            "phone" : "09151498722",
            "street" : "west coast street",
            "short_desc" : "test short desc",
            "desc" : "test description",
            "type" : "C",
            "state" : "C",
        }

        owner_2 = create_user("09151498721")
        create_cafe(self.province,self.city,self.owner,**payload)
        create_cafe(self.province,self.city,owner_2)
        
        url = get_cafe_city_url(self.city.slug)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        cafes = Cafe.objects.get_by_city(self.city.slug)
        self.assertEqual(len(cafes),1)
        self.assertTrue(cafes.exists())        

        
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