"""
Test Menu Item Endpoints
"""
import os
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

from cafe.models import (Cafe, Gallery)
from PIL import Image
import tempfile

from province.models import (City, Province)

GALLERY_URL = reverse('cafe:gallery-list')

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

def create_gallery(cafe,**new_payload):
    """Helper Function To Create Gallery"""
    payload = {
        "title" : "Test Gallery",
        "image" : "NoImage.jpg"
    }
    payload.update(new_payload)
    return Gallery.objects.create(cafe=cafe,**payload)

class PublicTest(TestCase):
    """Tests Which Does Not Need User To Be Authenticated"""
    def setUp(self):
        self.client = APIClient()
    
    def test_return_unauthorized(self):
        """Test if user is unauthorized"""
        res = self.client.get(GALLERY_URL)
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)

class PrivateTest(TestCase):
    """Tests Which Need User To Be Authenticated"""
    def setUp(self):
        self.client = APIClient()
        self.province = create_province("Tehran" , "Tehran")
        self.city = create_city("Tehran" , "Tehran",self.province)
        self.owner = create_user("09151498722",'123456')
        self.cafe = create_cafe(self.province,self.city,self.owner)
        self.client.force_authenticate(self.owner)

    def test_get_list_of_cafe_gallery(self):
        """Test Get List Of Cafe Gallery"""
        create_gallery(self.cafe)
        create_gallery(self.cafe)
        
        new_owner = create_user("09151498721","123456")
        new_cafe = create_cafe(self.province,self.city,new_owner)
        create_gallery(new_cafe)

        res = self.client.get(GALLERY_URL)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        
        galleries = Gallery.objects.filter(cafe_id=self.cafe.id).order_by('-id').values()
        # self.assertIn(galleries.first(),res.data)
        self.assertEqual(len(res.data['results']),2)
    
    def test_create_gallery_should_work_properly(self):
        """Test Create Gallery Should Work Properly"""
        payload = {
            "title" : "test gallery"
        }
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            img = Image.new('RGB' , (10,10))
            img.save(image_file,format='JPEG')
            image_file.seek(0)
            payload['image'] = image_file

            res = self.client.post(GALLERY_URL,payload,format='multipart')
            self.assertEqual(res.status_code , status.HTTP_201_CREATED)

            gallery = Gallery.objects.filter(cafe_id = self.cafe.id).first()
            self.assertEqual(gallery.cafe , self.cafe)

    def test_delete_gallery_should_work_properly(self):
        """Test Delete Gallery Should Work Properly"""
        gallery = create_gallery(self.cafe)
        old_img = gallery.image.path
        
        url = gallery_detail_url(gallery.id)
        res = self.client.delete(url)
        
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(os.path.exists(old_img))