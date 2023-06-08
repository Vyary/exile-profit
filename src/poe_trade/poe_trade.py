import json
from typing import Any, Dict, List, Tuple

import requests

from limiter.limiter import Limiter


class ApiClient:
    def make_api_request(
        self, request_type: str, url: str, query: Any
    ) -> requests.Response:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Content-Type": "application/json",
        }
        payload = json.dumps(query)
        return requests.request(request_type, url, headers=headers, data=payload)


class TradeSearcher:
    def search(
        self, league: str, limiter: Limiter, query: Dict[str, Any]
    ) -> Dict[str, Any] | None:
        trade_url = f"https://www.pathofexile.com/api/trade/search/{league}"
        response = ApiClient().make_api_request("POST", trade_url, query)

        if response.status_code != 200:
            return None

        limiter.rate_limiter(response)
        return response.json()


class ItemFetcher:
    def fetch_items(
        self, results_list: List[str], search_id: str
    ) -> Dict[str, Any] | None:
        items_link = (
            f"https://www.pathofexile.com/api/trade/fetch/"
            f"{','.join(results_list)}?query={search_id}"
        )
        response = ApiClient().make_api_request("GET", items_link, None)

        if response.status_code != 200:
            return None

        return response.json()


class CurrencyAliasesProvider:
    def get_currency_aliases(self) -> Dict[str, str]:
        static_data_url = "https://www.pathofexile.com/api/trade/data/static"
        response = ApiClient().make_api_request("GET", static_data_url, None)
        currency_data = json.loads(response.text)["result"]

        currency_aliases: Dict[str, str] = {}

        for currency_types in currency_data:
            for currency in currency_types["entries"]:
                full_name = currency["text"]
                short_name = currency["id"]
                currency_aliases[short_name] = full_name

        return currency_aliases


class League:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Content-Type": "application/json",
        }
        self.leagues_api = "https://www.pathofexile.com/api/trade/data/leagues"

    def current(self) -> str:
        try:
            leagues_api_response = requests.get(
                self.leagues_api, headers=self.headers
            ).json()
        except requests.exceptions.RequestException as e:
            return f"Error: , {e}"

        try:
            return leagues_api_response["result"][0]["id"]
        except KeyError:
            return "Error: Unable to retrieve the current league."


class PoeTrade:
    def __init__(
        self,
        league: str,
        limiter: Limiter,
        currency_prices: Dict[str, Any],
        trade_searcher: TradeSearcher,
        item_fetcher: ItemFetcher,
        currency_aliases_provider: CurrencyAliasesProvider,
    ):
        self.league = league
        self.limiter = limiter
        self.currency_prices = currency_prices
        self.trade_searcher = trade_searcher
        self.item_fetcher = item_fetcher
        self.currency_aliases = currency_aliases_provider.get_currency_aliases()

    def __make_api_request_and_collect_items_data(
        self, query: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], int] | Tuple[None, None]:
        search_response = self.trade_searcher.search(self.league, self.limiter, query)

        if search_response is None:
            return None, None

        total_listed = search_response["total"]
        search_id = search_response["id"]

        if total_listed < 12:
            results_list = search_response["result"][:10]
        else:
            results_list = search_response["result"][2:12]

        item_data = self.item_fetcher.fetch_items(results_list, search_id)
        return item_data, total_listed

    def __get_average_price(self, item_data: Dict[str, Any]) -> float:
        list_of_prices: List[float] = []

        for item in item_data["result"]:
            price = item["listing"]["price"]
            amount = price["amount"]
            type_of_currency = price["currency"]

            if type_of_currency != "chaos":
                if type_of_currency not in self.currency_aliases:
                    continue

                amount = (
                    amount
                    * self.currency_prices[self.currency_aliases[type_of_currency]][
                        "chaos"
                    ]
                )

            list_of_prices.append(amount)

        average_price = sum(list_of_prices) / len(item_data["result"])
        formatted_price = f"{average_price:.2f}"
        return float(formatted_price)

    def get_item_price(self, query: Dict[str, Any]) -> Tuple[float, int]:
        if not query:
            return 0, 0

        item_data, total_listed = self.__make_api_request_and_collect_items_data(query)

        if item_data is None:
            return 0, 0

        average_price = self.__get_average_price(item_data)
        return average_price, total_listed
