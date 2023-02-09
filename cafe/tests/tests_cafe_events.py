"""
Test Cafe Module Events
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta

from cafe.models import Cafe
from province.models import City, Province


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


class CafeEventsTest(TestCase):
    """Test Cafe Events"""

    def setUp(self):
        self.province = create_province("Tehran", "Tehran")
        self.city = create_city("Tehran", "Tehran", self.province)
        self.owner = create_user("09151498722")
        self.cafe = create_cafe(self.province, self.city, self.owner)

    def test_fill_unique_code_when_cafe_confirmed(self):
        """Test Fill Cafe Unique Code Whent Its confirmed"""
        self.cafe.state = "C"
        self.cafe.save()

        self.cafe.refresh_from_db()

        Cafe.objects.fill_unique_code(self.cafe.id)
        confirmed_cafe = Cafe.objects.filter(code=self.cafe.code).get()

        self.assertEqual(confirmed_cafe.state, "C")
        self.assertEqual(confirmed_cafe.id, self.cafe.id)
        self.assertTrue(len(self.cafe.code) == 5)

    def test_add_free_period_expired_date_to_cafe(self):
        """Test Add Free Period Expired Date To Cafe When Its Get Confirmed For First Time."""
        self.cafe.state = "C"
        self.assertFalse(self.cafe.charge_expired_date)

        self.cafe.charge_cafe(31, is_first=True)

        self.cafe.save()
        self.cafe.refresh_from_db()

        self.assertEqual(self.cafe.state, "C")
        self.assertTrue(self.cafe.charge_expired_date)
        self.assertEqual(
            self.cafe.charge_expired_date.date(),
            (datetime.now() + timedelta(days=31)).date(),
        )
