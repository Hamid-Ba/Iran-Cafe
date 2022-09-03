"""
Test account module models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

class UserTest(TestCase):
    """User Model Tests"""
    def test_create_user_should_work_properly(self):
        """Test Creating a Nromal User"""
        phone = "09151498722"
        password = "password123456"

        user = get_user_model().objects.create_user(phone=phone, password=password)

        self.assertEqual(user.phone , phone)
        self.assertTrue(user.check_password(password))