from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from ..models import Bonds


class IntegrationTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.bond = Bonds.objects.create(isin='RU1234567890', price=99.99)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_deal(self):
        data = {
            "buy": True,
            "quantity": 10,
            "bonds": self.bond.id
        }
        response = self.client.post(reverse('deals-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['buy'], data['buy'])
        self.assertEqual(response.data['quantity'], data['quantity'])
        self.assertEqual(response.data['bonds'], data['bonds'])
