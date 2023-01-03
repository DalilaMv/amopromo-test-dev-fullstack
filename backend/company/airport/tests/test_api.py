import unittest
from django.test.client import Client
from django.urls import reverse
import base64

class SimpleTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
 
    def test_details(self):
        endpoint = reverse('flight-query')
        
        response = self.client.get(
            f"{endpoint}?origin=AAX&destination=AJU&departure_date=2023-10-02&return_date=2023-10-10",
            HTTP_AUTHORIZATION= "Token eb4f768a22a1baaa4b485eb223af7fe308751da8"
        )
        
        self.assertTrue(response.status_code, 200)
