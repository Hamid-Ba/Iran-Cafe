"""
Test Plan Module Models
"""
from django.test import TestCase
from model_bakery import baker

from cloud import models

class CloudyCustomerTest(TestCase):
    """Test Cloudy Customer"""
    
    def setUp(self) -> None:
        self.cafe = baker.make("cafe.Cafe")
        return super().setUp()
    
    def test_create_cloudy_customer_should_work_properly(self):
        """Test Create Cloudy Customer"""
        payload = {
            "fullName" : "hamid balalzadeh",
            "phone": "09151498722",
            "cafe": self.cafe
        }
        
        cloudy_cafe = models.CloudyCustomer.objects.create(**payload)
        
        for key, value in payload.items():
            self.assertEqual(getattr(cloudy_cafe, key), value)
            
        self.assertFalse(cloudy_cafe.is_called)
        self.assertFalse(cloudy_cafe.is_confirmed)
        self.assertFalse(cloudy_cafe.is_cancelled)
        self.assertFalse(cloudy_cafe.is_deployed)