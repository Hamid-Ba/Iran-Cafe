"""
Test site info module models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

from siteinfo.models import AboutUs

class AboutUsTest(TestCase):
    """Test About Us Mode"""
    def test_create_aboutUs_model_should_work_properly(self):
        """Test Create About Us Model"""
        payload = {
            "text" : "Lorem ipsum dolor sit amet, consectetur adip",
            "phones" : "09151498722 , 09332829823",
            "emails" : "balalzadehhamid79@gmail.com , khosrora153333@gmail.com",
            "address" : "زاهدان زیباشهر نصر 11"
        }

        about_us = AboutUs.objects.create(**payload)

        for(key  , value) in payload.items():
            self.assertEqual(getattr(about_us, key), value)