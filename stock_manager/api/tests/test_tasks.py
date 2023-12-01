from decimal import Decimal

from django.test import TestCase
from unittest.mock import patch
from api.models import Bonds
from api.tasks import update_bonds


class UpdateBondsTest(TestCase):
    @patch('requests.get')
    def test_update_bonds(self, mock_get):
        # Mock the response from the API
        mock_get.return_value.json.return_value = {
            'marketdata_yields': {
                'columns': ["SECID", "BOARDID", "PRICE"],
                'data': [
                    ["RU000A0JX0J2", "TQCB", 99.37],
                    ["RU000A0JX0J3", "TQCB", 100.11]
                ]
            }
        }

        # Create some initial bonds
        Bonds.objects.create(isin='RU000A0JX0J2', price=100.00)
        Bonds.objects.create(isin='RU000A0JX0J3', price=100.00)

        # Run the task
        update_bonds()

        # Check that the prices have been updated
        self.assertEqual(Bonds.objects.get(isin='RU000A0JX0J2').price, Decimal('99.37'))
        self.assertEqual(Bonds.objects.get(isin='RU000A0JX0J3').price, Decimal('100.11'))
