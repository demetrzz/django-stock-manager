from celery import shared_task
import requests
from celery.utils.log import get_task_logger

from .models import Bonds

logger = get_task_logger(__name__)


@shared_task
def update_bonds():
    logger.info("sending request")
    response = requests.get(
        'https://iss.moex.com/iss/engines/stock/markets/bonds/boards/TQCB/securities.json?iss.meta=off')

    marketdata_yields = response.json()['marketdata_yields']

    marketdata_yields_data = []

    for data in marketdata_yields['data']:
        a = list(zip(marketdata_yields['columns'], data))
        marketdata_yields_data.append(a)
    logger.info('updating prices')
    for bond in marketdata_yields_data:
        Bonds.objects.filter(isin=bond[0][1]).update(price=bond[2][1])
