from typing import Dict

import requests


class CurrencyPrices:
    def __init__(self, league: str):
        self.league = league
        self.url: str = (
            f"https://poe.ninja/api/data/currencyoverview?league="
            f"{self.league}&type=Currency&language=en"
        )

    def get_currency_prices(self) -> Dict[str, float]:
        currency_prices: Dict[str, float] = {}

        response = requests.get(self.url).json()
        for currency in response["lines"]:
            currency_prices[currency["currencyTypeName"]] = currency["chaosEquivalent"]

        return currency_prices
