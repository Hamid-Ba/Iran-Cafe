"""
Test Plan Module Models
"""
from django.test import TestCase
from djmoney.money import Money

from plan import models


class PlanTest(TestCase):
    """Test Plan Model"""

    def test_create_plan_should_work_properly(self):
        """Test Create Plan Model"""
        payload = {
            "title": "Gold Plan",
            "period": 31,
            "image": "http://noImage.png",
            "price": Money(25000, "IRR"),
            "desc": "Gold Plan Description",
        }

        plan = models.Plan.objects.create(**payload)

        for key, value in payload.items():
            self.assertEqual(getattr(plan, key), value)

        self.assertTrue(plan.title)
        self.assertTrue(plan.price)
