from django.core.management import BaseCommand
from django.core.management.color import no_style
from django.db import connection

from api.models import Bonds
import requests


class Command(BaseCommand):
    def handle(self, **options):
        print("clearing db ...")
        Bonds.objects.all().delete()  # clear all database entries
        sequence_sql = connection.ops.sequence_reset_sql(no_style(), [Bonds])  # resetting PK to 0
        with connection.cursor() as cursor:
            for sql in sequence_sql:
                cursor.execute(sql)

        print("sending request")
        response = requests.get(
            'https://iss.moex.com/iss/engines/stock/markets/bonds/boards/TQCB/securities.json?iss.meta=off')

        marketdata_yields = response.json()['marketdata_yields']

        print("filling in market data")
        marketdata_yields_data = []

        for data in marketdata_yields['data']:
            a = list(zip(marketdata_yields['columns'], data))  # filling in market data
            marketdata_yields_data.append(a)

        # here we check if data exists, if it doesn't or exceeds reasonable numbers then we don't add
        for bond in marketdata_yields_data:
            if bond[6][1] and bond[6][1] < 40:
                pass
            else:
                continue

            if bond[9][1] and (20 > bond[9][1] / 100 > -20):
                pass
            else:
                continue

            if bond[8][1] and (20 > bond[8][1] / 100 > -20):
                pass
            else:
                continue

            if bond[2][1] and bond[7][1] and bond[3][1]:
                pass
            else:
                continue

            if bond[0][1].startswith('RU'):
                pass
            else:
                continue

            Bonds.objects.update_or_create(
                isin=bond[0][1],
                price=bond[2][1],
            )
