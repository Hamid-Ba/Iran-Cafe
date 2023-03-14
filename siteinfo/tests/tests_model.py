"""
Test site info module models
"""
from django.test import TestCase

from siteinfo.models import AboutUs, ContactUs


class AboutUsTest(TestCase):
    """Test About Us Model"""

    def test_create_aboutUs_model_should_work_properly(self):
        """Test Create About Us Model"""
        payload = {
            "text": "Lorem ipsum dolor sit amet, consectetur adip",
            "phones": "09151498722 , 09332829823",
            "emails": "balalzadehhamid79@gmail.com , khosrora153333@gmail.com",
            "address": "زاهدان زیباشهر نصر 11",
        }

        about_us = AboutUs.objects.create(**payload)

        for key, value in payload.items():
            self.assertEqual(getattr(about_us, key), value)


class ContactUsTest(TestCase):
    """Test Contact Us Model"""

    def test_create_contact_us_model_should_work_properly(self):
        """Test Create Contact Us Model"""
        payload = {
            "full_name": "John Smith",
            "phone": "09151498722",
            "message": "Thank you for your contact information",
        }

        contact_us = ContactUs.objects.create(**payload)

        for key, value in payload.items():
            self.assertEqual(getattr(contact_us, key), value)
