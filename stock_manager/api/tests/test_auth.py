from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User


class AuthenticationTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = APIClient()

    def test_authenticated_user_can_access_deals_viewset(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('deals-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_user_cannot_access_deals_viewset(self):
        response = self.client.get(reverse('deals-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
