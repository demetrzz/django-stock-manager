from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Bonds, Deals


class BondsModelTest(TestCase):
    def setUp(self):
        self.bond = Bonds.objects.create(isin='RU1234567890', price=99.99)

    def test_bonds_creation(self):
        self.assertEqual(self.bond.isin, 'RU1234567890')
        self.assertEqual(self.bond.price, 99.99)


class DealsModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.bond = Bonds.objects.create(isin='RU1234567890', price=99.99)
        self.deal = Deals.objects.create(buy=True, quantity=10, price_at_the_time=99.99,
                                         bonds=self.bond, user=self.user)

    def test_deals_creation(self):
        self.assertEqual(self.deal.buy, True)
        self.assertEqual(self.deal.quantity, 10)
        self.assertEqual(self.deal.price_at_the_time, 99.99)
        self.assertEqual(self.deal.bonds, self.bond)
        self.assertEqual(self.deal.user, self.user)
