from django.test import TestCase
from unittest.mock import patch
from api.models import Bonds
from django.core.management import call_command
from decimal import Decimal


class CommandTestCase(TestCase):
    @patch('requests.get')
    def test_command(self, mock_get):
        # Mock the response from the API
        mock_get.return_value.json.return_value = {
            'marketdata_yields': {
                'columns': ["SECID", "BOARDID", "PRICE", "YIELDDATE", "ZCYCMOMENT", "YIELDDATETYPE", "EFFECTIVEYIELD", "DURATION", "ZSPREADBP", "GSPREADBP", "WAPRICE", "EFFECTIVEYIELDWAPRICE", "DURATIONWAPRICE", "IR", "ICPI", "BEI", "CBR", "YIELDTOOFFER", "YIELDLASTCOUPON", "TRADEMOMENT", "SEQNUM", "SYSTIME"],
                'data': [
                    ["RU000A0JX0J2", "TQCB", 99.37, "2024-07-08", "2023-11-30 18:39:57", "MATDATE", 13.3321, 212, 142, 139, 97, 13.5845, 212, None, None, None, None, None, None, "2023-11-30 18:45:06", 20231130190000, "2023-11-30 19:00:00"],
                    ["RU000A0JX0J3", "TQCB", 100.11, "2024-07-08", "2023-11-30 18:39:57", "MATDATE", 13.3321, 212, 142, 139, 97, 13.5845, 212, None, None, None, None, None, None, "2023-11-30 18:45:06", 20231130190000, "2023-11-30 19:00:00"]
                ]
            }
        }

        # Run the command
        call_command('db_data_initialization')

        # Check that the bonds have been created
        self.assertEqual(Bonds.objects.get(isin='RU000A0JX0J2').price, Decimal('99.37'))
        self.assertEqual(Bonds.objects.get(isin='RU000A0JX0J3').price, Decimal('100.11'))
