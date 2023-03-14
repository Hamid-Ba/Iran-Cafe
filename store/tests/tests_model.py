# import necessary modules
from django.test import TestCase
from store import models


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
        self.assertEqual(self.category.sub_category.title, "TestSubCategory")
