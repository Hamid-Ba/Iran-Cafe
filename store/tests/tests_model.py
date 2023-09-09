# import necessary modules
from uuid import uuid4
from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal

from cafe.models import Cafe
from province.models import City, Province
from store import models


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
        "state": "C",
        "province": province,
        "city": city,
        "owner": owner,
    }
    payload.update(new_payload)
    return Cafe.objects.create(**payload)


# create a class to test the category model
class TestStoreCategory(TestCase):
    def setUp(self):
        # create a category object with test values
        self.category = models.StoreCategory.objects.create(
            title="TestCategory",
            sortitem=1,
            sub_category=models.StoreCategory.objects.create(
                title="TestSubCategory", sortitem=2
            ),
        )

    def tearDown(self):
        # delete the created category object
        self.category.delete()

    def test_category_title(self):
        # check if the category title is correct
        self.assertEqual(self.category.title, "TestCategory")

    def test_category_sortitem(self):
        # check if the category sort item is correct
        self.assertEqual(self.category.sortitem, 1)

    def test_category_sub_category(self):
        # check if the category sub category is correct
        self.assertEqual(str(self.category.sub_category), "TestSubCategory")


class ProductTest(TestCase):
    def setUp(self):
        self.category = models.StoreCategory.objects.create(
            title="Test Category", sortitem=1
        )
        self.product = models.Product.objects.create(
            title="Test Product",
            desc="This is a test product.",
            price=Decimal(100),
            image_url="https://example.com/images/test.png",
            category=self.category,
        )

    def test_product_creation(self):
        self.assertEqual(models.Product.objects.count(), 1)

    def test_product_str(self):
        self.assertEqual(str(self.product), "Test Product")


class StoreOrderTest(TestCase):
    def setUp(self):
        self.province = create_province("Tehran", "Tehran")
        self.city = create_city("Tehran", "Tehran", self.province)
        self.owner = create_user("09151498722")
        self.cafe = create_cafe(self.province, self.city, self.owner)

        self.order = models.StoreOrder.objects.create(
            state=models.StoreOrder.OrderState.PENDING,
            code=str(uuid4())[:5],
            total_price=1000,
            address="123 Test St",
            postal_code="12345",
            fullName="Hamid Balalzadeh",
            cafe=self.cafe,
            user=self.owner,
        )

    def test_store_order_string_representation(self):
        self.assertEqual(
            str(self.order), f"Store Order #{self.order.pk}-{self.order.code}"
        )

    def test_store_order_code_not_null(self):
        self.assertIsNotNone(self.order.code)

    def test_store_order_item_relation(self):
        item = models.StoreOrderItem.objects.create(
            product_id=1,
            title="Test Item",
            image_url="https://test.com/image.jpg",
            desc="Test Description",
            price=500,
            count=2,
            order=self.order,
        )
        self.assertIn(item, self.order.items.all())
