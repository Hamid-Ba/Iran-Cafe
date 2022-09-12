"""
Test Category Endpoints
"""
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from cafe.models import Category
from cafe.serializers import CateogrySerializer

CATEGORY_LIST = reverse('cafe:category_list')

def create_category(title):
    """Helper Function For Create Category"""
    return Category.objects.create(title=title)

class PublicTest(TestCase):
    """Test Category Public Endpoints"""
    def setUp(self):
        self.client = APIClient()

    def test_get_category_list_should_work_properly(self):
        """Test Get Category List"""
        category1 = create_category('category1')
        category2 = create_category('category2')

        res = self.client.get(CATEGORY_LIST)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        categories = Category.objects.all().order_by('-id')
        serializer = CateogrySerializer(categories,many=True)

        self.assertEqual(serializer.data,res.data)