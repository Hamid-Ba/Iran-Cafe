"""
Test Bartender Endpoints
"""
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from cafe.models import Bartender, Cafe

from province.models import City, Province

BARTENDER_URL = reverse("cafe:bartender-list")


def get_cafe_province_url(slug):
    return reverse("cafe:cafes_by_province", kwargs={"province_slug": slug})


def get_cafe_city_url(slug):
    return reverse("cafe:cafes_by_city", kwargs={"city_slug": slug})


def get_cafe_url_by_code(code):
    """Return Cafe URL By Unique Code."""
    return reverse("cafe:cafe_id", kwargs={"cafe_code": code})


def get_cafe_url_by_id(cafe_id):
    """Return Cafe URL By Unique Code."""
    return reverse("cafe:cafe_detail_page", kwargs={"cafe_id": cafe_id})


def create_user(phone, password=None):
    """Helper Function For Create User"""
    return get_user_model().objects.create_user(phone=phone, password=password)


def create_province(name, slug):
    """Helper Function To Create Province"""
    return Province.objects.create(name=name, slug=slug)


def create_city(name, slug, province):
    """Helper Function To Create Province"""
    return City.objects.create(name=name, slug=slug, province=province)


def create_cafe(province, city, owner, **new_payload):
    """Helper Function To Create Cafe"""
    payload = {
        "persian_title": "تست",
        "english_title": "Test",
        "phone": owner.phone,
        "street": "west coast street",
        "desc": "test description",
        "type": "C",
        "state": "P",
        "province": province,
        "city": city,
        "owner": owner,
    }
    payload.update(new_payload)
    return Cafe.objects.create(**payload)


class PublicTest(TestCase):
    """Tests Which Does Not Need User To Be Authenticated"""

    def setUp(self):
        self.client = APIClient()

    def test_return_unauthorized(self):
        """Test if user is unauthorized"""
        res = self.client.get(BARTENDER_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_unauthorized(self):
        """Test if user is unauthorized"""
        res = self.client.post(BARTENDER_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTest(TestCase):
    """Tests Which Need User To Be Authenticated"""

    def setUp(self):
        self.client = APIClient()
        self.province = create_province("Tehran", "Tehran")
        self.city = create_city("Tehran", "Tehran", self.province)
        self.owner = create_user("09151498722", "123456")
        self.client.force_authenticate(self.owner)
        self.cafe = create_cafe(self.province, self.city, self.owner)

    def test_create_bartender_should_work_properly(self):
        """Test Create Bartender"""
        payload = {"phone": "09151498721"}

        res = self.client.post(BARTENDER_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.filter(phone=payload["phone"]).first()
        self.assertTrue(user)

        bartneder = Bartender.objects.filter(user=user).first()

        self.assertTrue(bartneder)
        self.assertEqual(bartneder.phone, payload["phone"])
        self.assertTrue(bartneder.cafe.owner, self.owner)
