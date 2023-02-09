"""
Test Contact Us Module
"""
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status

from siteinfo.models import ContactUs

CONTACT_US_URL = reverse("site_info:contact_us")


class PublicTest(TestCase):
    """Test Cases Which Doesnt Need User To Be Authenticated"""

    def setUp(self):
        self.client = APIClient()

    def test_create_contactUs_should_work_properly(self):
        """Test Create Contact Us"""
        payload = {
            "full_name": "John Smith",
            "phone": "09151498722",
            "message": "Hello, John Smith!",
        }

        res = self.client.post(CONTACT_US_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        contact_us = (
            ContactUs.objects.filter(phone=payload["phone"]).order_by("-id").first()
        )
        for key, value in payload.items():
            self.assertEqual(getattr(contact_us, key), value)
