"""
Test Blog Module Models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import (date)

from blog import models

def create_user(phone,password):
    """Helper Function for creating a user"""
    return get_user_model().objects.create_user(phone=phone,password=password)

class BlogModel(TestCase):
    """Test Blog Model"""
    def test_blog_model_should_work_properly(self):
        """Test Blog Model"""
        user = create_user('09151498721','123456')
        payload = {
            'title' : 'Test Blog Model',
            'slug' : 'Test-Blog-Model',
            'cafe_id' : 2,
            'desc' : 'Test Blog Model',
            'image' : 'blog.png',
            'image_alt' : 'blog',
            'image_title' : 'blog',
            'is_cafe' : False,
            'publish_date' : date(2022,6,12),
            'tags' : ['blog','cafe','food'],
            'user' : user,
        }

        blog = models.Blog.objects.create(**payload)

        for (key  , value) in payload.items():
            self.assertEqual(getattr(blog, key), value)