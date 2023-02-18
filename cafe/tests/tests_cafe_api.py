"""
Test Cafe Endpoints
"""
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from datetime import datetime, timedelta
from rest_framework import status
from django.contrib.auth import get_user_model

from cafe.models import Bartender, Cafe
from cafe.serializers import CafeSerializer
from province.models import City, Province

CAFE_URL = reverse("cafe:cafe-list")


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


def create_bartender(phone, cafe):
    user = create_user(phone, "123456")
    return Bartender.objects.create(phone=phone, user=user, cafe=cafe)


class PublicTest(TestCase):
    """Test Those Endpoints Which Don't Need User To Be Authorized"""

    def setUp(self):
        self.client = APIClient()
        self.province = create_province("Tehran", "Tehran")
        self.city = create_city("Tehran", "Tehran", self.province)
        self.owner = create_user("09151498722")

    def test_get_cafes_by_province_should_work_properly(self):
        """Test Gets Cafe By Province"""
        payload = {
            "persian_title": "تست",
            "english_title": "Test",
            "street": "west coast street",
            "desc": "test description",
            "type": "C",
            "state": "C",
        }

        province_2 = create_province("NY", "NY")
        city_2 = create_city("SD", "SD", province_2)
        owner_2 = create_user("09151498721")

        create_cafe(self.province, self.city, self.owner, **payload)
        create_cafe(province_2, city_2, owner_2, **payload)

        url = get_cafe_province_url(self.province.slug)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        cafes = Cafe.objects.get_by_province(self.province.slug)
        self.assertEqual(len(cafes), 1)
        self.assertTrue(cafes.exists())

    def test_get_empty_cafe_list_by_province(self):
        """Test If Provinces Cafe Are None"""
        url = get_cafe_province_url(self.province.slug)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_cafes_list_if_cafe_confirmed__and_charged(self):
        """Test If Cafe Is Confirmed Then Show It"""
        payload = {
            "persian_title": "تست",
            "english_title": "Test",
            "phone": "09151498722",
            "street": "west coast street",
            "desc": "test description",
            "type": "C",
            "state": "C",
        }

        owner_2 = create_user("09151498721")
        create_cafe(self.province, self.city, self.owner, **payload)
        create_cafe(self.province, self.city, owner_2)

        owner_3 = create_user("09151498723")
        not_charged_cafe = create_cafe(
            self.province, self.city, owner_3, **{"state": "C"}
        )
        not_charged_cafe.charge_expired_date = datetime.now() - timedelta(days=5)
        not_charged_cafe.save()

        owner_4 = create_user("09151498724")
        charged_cafe = create_cafe(self.province, self.city, owner_4, **{"state": "C"})
        charged_cafe.charge_expired_date = datetime.now() + timedelta(days=5)
        charged_cafe.save()

        url = get_cafe_province_url(self.province.slug)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        cafes = Cafe.objects.get_by_province(self.province.slug)
        self.assertEqual(len(cafes), 2)
        self.assertTrue(cafes.exists())

    def test_filter_by_city_name_type(self):
        """Test Filter Cafes By City Name Type"""
        payload = {
            "persian_title": "تست",
            "english_title": "Test",
            "phone": "09151498722",
            "street": "west coast street",
            "desc": "test description",
            "type": "C",
            "state": "C",
        }
        payload2 = {
            "persian_title": "2تست",
            "english_title": "Test2",
            "phone": "09151498721",
            "street": "west coast street",
            "desc": "test description",
            "type": "R",
            "state": "C",
        }
        payload3 = {
            "persian_title": "3تست",
            "english_title": "Test3",
            "phone": "09151498723",
            "street": "west coast street",
            "desc": "test description",
            "type": "C",
            "state": "C",
        }

        owner_2 = create_user("09151498721")
        city_2 = create_city("Shahriar", "Shahriar", self.province)
        owner_3 = create_user("09151498723")
        c1 = create_cafe(self.province, self.city, self.owner, **payload)
        c2 = create_cafe(self.province, self.city, owner_2, **payload2)
        c3 = create_cafe(self.province, city_2, owner_3, **payload3)

        params = {"city": self.city.id, "title": "تست", "type": "C"}
        url = get_cafe_province_url(self.province.slug)
        res = self.client.get(url, params)

        s1 = CafeSerializer(c1)
        s2 = CafeSerializer(c2)
        s3 = CafeSerializer(c3)

        self.assertEqual(len(res.data), 1)
        self.assertEqual(s1.data["id"], res.data[0]["id"])
        self.assertNotEqual(s2.data["id"], res.data[0]["id"])
        self.assertNotEqual(s3.data["id"], res.data[0]["id"])

    def test_get_cafe_by_city_should_work_properly(self):
        """Test Get Cafe List Filterd By City"""
        payload = {
            "persian_title": "تست",
            "english_title": "Test",
            "street": "west coast street",
            "desc": "test description",
            "type": "C",
            "state": "C",
        }

        province_2 = create_province("NY", "NY")
        city_2 = create_city("SD", "SD", province_2)
        owner_2 = create_user("09151498721")

        create_cafe(self.province, self.city, self.owner, **payload)
        create_cafe(province_2, city_2, owner_2)

        url = get_cafe_city_url(self.city.slug)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        cafes = Cafe.objects.get_by_city(self.city.slug)
        self.assertEqual(len(cafes), 1)
        self.assertTrue(cafes.exists())

    def test_get_empty_cafe_list_by_city(self):
        """Test Get None Cafe If No Cafe Registered In City"""
        url = get_cafe_city_url(self.city.slug)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_cafe_list_by_city_if_cafe_confirmed(self):
        """Test Get Confirmed Cafes"""
        payload = {
            "persian_title": "تست",
            "english_title": "Test",
            "phone": "09151498722",
            "street": "west coast street",
            "desc": "test description",
            "type": "C",
            "state": "C",
        }

        owner_2 = create_user("09151498721")
        create_cafe(self.province, self.city, self.owner, **payload)
        create_cafe(self.province, self.city, owner_2)

        url = get_cafe_city_url(self.city.slug)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        cafes = Cafe.objects.get_by_city(self.city.slug)
        self.assertEqual(len(cafes), 1)
        self.assertTrue(cafes.exists())

    def test_return_cafe_id_by_code(self):
        """Test Return Cafe Id By Unique Code"""
        payload = {
            "persian_title": "تست",
            "code": "12345",
            "english_title": "Test",
            "phone": "09151498722",
            "street": "west coast street",
            "desc": "test description",
            "type": "C",
            "state": "C",
        }

        owner_2 = create_user("09151498721")
        cafe2 = create_cafe(self.province, self.city, owner_2)

        cafe = create_cafe(self.province, self.city, self.owner, **payload)
        cafe.charge_expired_date = datetime.now() + timedelta(days=5)
        cafe.save()

        url = get_cafe_url_by_code(cafe.code)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(cafe.id, res.data["id"])
        self.assertNotEqual(cafe2.id, res.data["id"])

    def test_return_cafe_id_by_code_if_cafe_not_charged(self):
        """Test Return Cafe Id By Unique Code If Charged"""
        payload = {
            "persian_title": "تست",
            "code": "12345",
            "english_title": "Test",
            "phone": "09151498722",
            "street": "west coast street",
            "desc": "test description",
            "type": "C",
            "state": "C",
        }

        cafe = create_cafe(self.province, self.city, self.owner, **payload)
        cafe.charge_expired_date = datetime.now() - timedelta(days=5)
        cafe.save()

        url = get_cafe_url_by_code(cafe.code)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_cafe_view_count(self):
        """Test Add View Count"""
        cafe = create_cafe(self.province, self.city, self.owner, **{"state": "C"})
        cafe.charge_expired_date = datetime.now() + timedelta(days=5)
        cafe.save()

        url = get_cafe_url_by_id(cafe.id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        cafe.refresh_from_db()
        self.assertEqual(cafe.view_count, 1)

    def test_fast_register(self):
        """Test Register User Within Cafe Concurrently"""
        payload = {
            # "code" : str(uuid.uuid1())[0:5],
            "persian_title": "تست",
            "english_title": "Test",
            "phone": "09151498722",
            "street": "west coast street",
            "desc": "test description",
            "type": "C",
            "province": self.province.id,
            "city": self.city.id,
        }

        url = reverse("cafe:fast_register")
        res = self.client.post(url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        owner = get_user_model().objects.filter(phone=payload["phone"]).first()
        cafe = Cafe.objects.filter(owner=owner).first()

        self.assertTrue(owner)
        self.assertTrue(cafe)

        for key, value in payload.items():
            if not (key == "province" or key == "city"):
                self.assertEqual(getattr(cafe, key), value)

        self.assertEqual(cafe.state, "P")


class PrivateTest(TestCase):
    """Test Those Endpoints Which Need User To Be Authorized"""

    def setUp(self):
        self.client = APIClient()
        self.owner = create_user("09151498722")
        self.province = create_province("Tehran", "Tehran")
        self.city = create_city("Tehran", "Tehran", self.province)

    def test_register_cafe_should_work_properly(self):
        """Test Registering The Cafe By User"""
        self.client.force_authenticate(self.owner)

        payload = {
            # "code" : str(uuid.uuid1())[0:5],
            "persian_title": "تست",
            "english_title": "Test",
            "phone": "09151498722",
            "street": "west coast street",
            "desc": "test description",
            "type": "C",
            "province": self.province.id,
            "city": self.city.id,
        }

        res = self.client.post(CAFE_URL, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Cafe.objects.filter(owner=self.owner).exists())

    def test_bartender_can_not_register_cafe(self):
        """Test Bartander Can Not Register Cafe"""
        cafe = Cafe.objects.create(
            owner=self.owner, province=self.province, city=self.city
        )
        bartender = create_bartender("09151498721", cafe)
        self.client.force_authenticate(bartender.user)
        payload = {
            # "code" : str(uuid.uuid1())[0:5],
            "persian_title": "تست",
            "english_title": "Test",
            "phone": "09151498721",
            "street": "west coast street",
            "desc": "test description",
            "type": "C",
            "province": self.province.id,
            "city": self.city.id,
        }

        res = self.client.post(CAFE_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(Cafe.objects.filter(owner=bartender.user).exists())
