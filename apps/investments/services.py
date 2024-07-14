from typing import Dict
import requests
from django.conf import settings


class CurrencyService:
    @staticmethod
    def get_currency_values() -> Dict[str, float]:
        url = settings.EXCHANGERATESAPI_HOST

        params = {"access_key": settings.EXCHANGERATESAPI_KEY}

        response = requests.get(url, params=params)

        if response.status_code == 200:
            currencies = response.json()["rates"]
            return currencies

        raise Exception()
