"""
Test Province Module
"""
from django.test import TestCase
from province.models import (Province , City)

def create_province(name):
    """Helper Function To Create Province"""
    return Province.objects.create(name=name)

class ProvinceTest(TestCase):
    """Test Province Model"""

    def test_create_province_should_work_propely(self):
        """Test To Create Province Object"""
        name = 'tehran'
        province = Province.objects.create(name=name)
        self.assertEqual(province.name , name)

class CityTest(TestCase):
    """Test City Model"""

    def test_create_city_should_work_propely(self):
        """Test To Create City Object"""
        province = create_province(name='sistan va baluchestan')
        city_name = 'zahedan'

        city = City.objects.create(name=city_name,province=province)

        self.assertEqual(city.name, city_name)
        self.assertEqual(city.province.name , province.name)

