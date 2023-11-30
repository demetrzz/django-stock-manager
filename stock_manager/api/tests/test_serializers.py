from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Bonds, Deals
from ..serializers import DealsSerializer, BondsSerializer


class DealsSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.bond = Bonds.objects.create(isin='RU1234567890', price=99.99)
        self.deal = Deals.objects.create(buy=True, quantity=10, price_at_the_time=99.99,
                                         bonds=self.bond, user=self.user)
        self.serializer = DealsSerializer(instance=self.deal)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['id', 'buy', 'quantity',
                                            'price_at_the_time', 'time_create', 'bonds', 'user'])

    def test_buy_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['buy'], self.deal.buy)


class BondsSerializerTest(TestCase):
    def setUp(self):
        self.bond = Bonds.objects.create(isin='RU1234567890', price=99.99)
        self.serializer = BondsSerializer(instance=self.bond)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['id', 'isin', 'price', 'time_create', 'time_update'])

    def test_isin_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['isin'], self.bond.isin)
