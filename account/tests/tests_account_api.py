"""
Tests Account Module APIs
"""
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

AUTH_URL = reverse('account:auth-login-or-register')
TOKEN_URL = reverse('account:token')

def create_user(phone,password=None):
    """Helper Function For Create User"""
    return get_user_model().objects.create_user(phone=phone,password=password)

class PublicTests(TestCase):
    """Test Cases which doesn't require authentication"""
    def setUp(self):
        self.client = APIClient()

    def test_register_should_work_properly(self):
        """Test User Registeration"""
        payload = {
            'phone' : '09151498722',
        }

        res = self.client.post(AUTH_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_200_OK)

        is_user_exist = get_user_model().objects.filter(phone=payload['phone']).exists()
        self.assertTrue(is_user_exist)

    def test_login_should_work_properly(self):
        """Test User Login"""
        payload = {
            'phone' : '09151498722',
        }
        user = create_user(payload['phone'],password='123456')
        old_password = user.password

        res = self.client.post(AUTH_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_200_OK)

        user.refresh_from_db()
        self.assertNotEqual(user.password , old_password)

    def test_create_token_should_work_properly(self):
        """Test For Creation The Token"""
        payload = {
            "phone" : "09151498722",
            "password" : "123456"
        }

        user = create_user(payload['phone'],payload['password'])

        res = self.client.post(TOKEN_URL,payload)
        
        self.assertIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_200_OK)