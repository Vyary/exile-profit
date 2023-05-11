import json
from typing import Any, Dict, List

import requests
from requests import Response

from utils.limiter.limiter import Limiter
from utils.price_check.api_call import APICall


class PoeTrade(APICall):
    def __init__(
        self, league: str, currency_prices: Dict[str, float], limiter: Limiter
    ):
        self.league = league
        self.currency_prices = currency_prices
        self.limiter = limiter
        self.initial_url: str = (
            f"https://www.pathofexile.com/api/trade/search/{self.league}"
        )
        self.headers: Dict[str, str] = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Content-Type": "application/json",
        }

    def __make_api_request_and_collect_items_data(
        self, query: Dict[str, Any]
    ) -> Response:
        payload = json.dumps(query)
        get_results_ids = requests.request(
            "POST", self.initial_url, headers=self.headers, data=payload
        )

        # check ip state
        self.limiter.rate_limiter(get_results_ids)

        search_id = json.loads(get_results_ids.text)["id"]
        results_list = json.loads(get_results_ids.text)["result"][2:12]

        # link to listed items and prices
        items_link = (
            f"https://www.pathofexile.com/api/trade/fetch/"
            f"{','.join(results_list)}?query={search_id}"
        )

        # get request for the actual listings
        api_response = requests.request("GET", items_link, headers=self.headers)

        return api_response

    def __get_average_price(self, api_response: Response) -> float:
        item_data = json.loads(api_response.text)["result"]

        list_of_prices: List[float] = []

        for item in item_data:
            amount = item["listing"]["price"]["amount"]
            type_of_currency = item["listing"]["price"]["currency"]

            if type_of_currency != "chaos":
                type_of_currency = type_of_currency.split("-")[0]
                currency_before = f"{type_of_currency} not found"

                if type_of_currency == "gcp":
                    currency_before = "Gemcutter's Prism"

                # TODO: Change from loop to dict
                for currency in self.currency_prices:
                    if type_of_currency in currency.lower():
                        currency_before = currency
                        break

                type_of_currency_to_chaos_orbs = self.currency_prices[currency_before]

                price_in_chaos_orbs = amount * type_of_currency_to_chaos_orbs
                list_of_prices.append(price_in_chaos_orbs)
                continue

            list_of_prices.append(amount)

        average_price = sum(list_of_prices) / len(item_data)
        formatted_price = f"{average_price:.2f}"
        return float(formatted_price)

    def get_price(self, query: Dict[str, Any]) -> float:
        api_response = self.__make_api_request_and_collect_items_data(query)
        average_price = self.__get_average_price(api_response)
        return average_price
