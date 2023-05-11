from typing import Any, Dict


class CurrencyExchange:
    @staticmethod
    def get_exchange_currency_data(
        exchangeable_currencies: Dict[str, Any], currency_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        for currency in exchangeable_currencies:
            exchangeable_currencies[currency]["currency_value"] = currency_data[
                currency
            ]

            component = exchangeable_currencies[currency]["component"]
            exchangeable_currencies[currency]["component_price"] = currency_data[
                component
            ]

            currency_value = exchangeable_currencies[currency]["currency_value"]
            component_price = exchangeable_currencies[currency]["component_price"]
            component_count = exchangeable_currencies[currency]["component_count"]
            exchangeable_currencies[currency]["profit_per_100"] = (
                currency_value - (float(component_count) * float(component_price))
            ) * 100

        return exchangeable_currencies
