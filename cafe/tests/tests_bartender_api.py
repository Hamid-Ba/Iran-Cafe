"""
Test Bartender Endpoints
"""
from uuid import uuid4
from django.test import TestCase
# from decimal import Decimal
from djmoney.money import Money
from datetime import (datetime , time)
from django.contrib.auth import get_user_model
from cafe.models import (Bartender, Cafe , Category, MenuItem , Gallery, Order, Suggestion , Reservation)
from province.models import (Province , City)

class PublicTest(TestCase):
    """Test Category Public Endpoints"""