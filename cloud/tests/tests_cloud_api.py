"""
Test Cloud Endpoints
"""
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from model_bakery import baker
from rest_framework import status

from cloud import models, serializers

CLOUD_URL = reverse("cloud:cloudy")


class PublicTest(TestCase):
    """Cloud Public Test"""

    def setUp(self):
        self.client = APIClient()

    def test_return_unauthorized(self):
        """Return UnAuthorized Access"""
        res = self.client.get(CLOUD_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTest(TestCase):
    """Cloud Private Test"""

    def setUp(self):
        owner = baker.make("account.User")
        self.cafe = baker.make("cafe.Cafe", owner=owner)

        self.client = APIClient()
        self.client.force_authenticate(owner)

        self.payload = {"fullName": "Hamid Balalzadeh"}

    def test_get_exist_cloud_request_should_work_properly(self):
        """Test Get Cloudy Customer If Exist"""
        cloud = baker.make(models.CloudyCustomer, cafe=self.cafe, **self.payload)

        res = self.client.get(CLOUD_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        serializer = serializers.CloudyCustomerSerializer(cloud, many=False)
        self.assertEqual(res.data, serializer.data)

    def test_create_cloud_request_should_work_properly(self):
        """Test Creation Of Cloudy Customer"""
        res = self.client.post(CLOUD_URL, self.payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        cloud = models.CloudyCustomer.objects.last()

        for key, value in self.payload.items():
            self.assertEqual(getattr(cloud, key), value)

    def test_create_existing_cloud_request_should_return_bad_request(self):
        """Test Creation Of Existing Cloudy Customer"""
        baker.make(models.CloudyCustomer, cafe=self.cafe, **self.payload)

        res = self.client.post(CLOUD_URL, self.payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
