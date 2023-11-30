from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from ..models import Bonds, Deals


class DealsViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.bond = Bonds.objects.create(isin='RU1234567890', price=99.99)
        self.deal = Deals.objects.create(buy=True, quantity=10,
                                         price_at_the_time=99.99, bonds=self.bond, user=self.user)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_list_deals(self):
        response = self.client.get(reverse('deals-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class BondsViewSetTest(APITestCase):
    def setUp(self):
        self.bond = Bonds.objects.create(isin='RU1234567890', price=99.99)
        self.client = APIClient()

    def test_list_bonds(self):
        response = self.client.get(reverse('bonds-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
