from typing import Dict

import requests


class PoeNinjaAPI:
    def __init__(self, current_league: str):
        self.current_league = current_league

    def get_response(self, url: str):
        response = requests.get(url)
        response.raise_for_status()  # raise an exception if the request fails
        return response.json()


class MassiveData:
    def __init__(self, api: PoeNinjaAPI):
        self.api = api

    def get_massive_data(self) -> Dict[str, Dict[str, str]]:
        url = (
            f"https://poe.ninja/api/data/DenseOverviews?league="
            f"{self.api.current_league}&language=en"
        )
        response = self.api.get_response(url)
        massive_data: Dict[str, Dict[str, str]] = {}

        for sub_dict in response["currencyOverviews"] + response["itemOverviews"]:
            for item in sub_dict["lines"]:
                massive_data[item["name"]] = item
        return massive_data


class DivinationCards:
    def __init__(self, api: PoeNinjaAPI):
        self.api = api

    def get_divination_cards_data(self) -> Dict[str, Dict[str, str | float]]:
        url = (
            f"https://poe.ninja/api/data/itemoverview?league={self.api.current_league}"
            "&type=DivinationCard&language=en"
        )
        response = self.api.get_response(url)

        div_card_dict_from_response: Dict[str, Dict[str, str]] = {
            f'{card["name"]}': card for card in response["lines"]
        }

        cleaned_div_card_data: Dict[str, Dict[str, str | float]] = {}

        for card_name, card in div_card_dict_from_response.items():
            stack_size = card.get("stackSize", 1)
            card_price = card["chaosValue"]
            reward_count = 1
            raw_info = str(card["explicitModifiers"][0])
            reward = raw_info[raw_info.find(">{") + 2 : raw_info.find("}")]

            if ">{" in reward:
                reward_list = reward.split(">{")
                reward = reward_list[1]
            if "x " in reward:
                reward_count, reward = reward.split("x ")

            cleaned_div_card_data[card_name] = {
                "name": card_name,
                "stack_size": stack_size,
                "card_price": card_price,
                "reward_count": reward_count,
                "reward": reward,
            }

        return cleaned_div_card_data


class SkillGems:
    def __init__(self, api: PoeNinjaAPI):
        self.api = api

    def get_gems_data(self):
        url = (
            f"https://poe.ninja/api/data/itemoverview?league={self.api.current_league}"
            "&type=SkillGem&language=en"
        )
        response = self.api.get_response(url)

        gems_data_dict = {
            f'{gem["name"]}|{gem["variant"]}': gem for gem in response["lines"]
        }

        return gems_data_dict


class CurrencyPrices:
    def __init__(self, api: PoeNinjaAPI):
        self.api = api

    def get_currency_prices(self) -> Dict[str, float]:
        url: str = (
            f"https://poe.ninja/api/data/currencyoverview?league="
            f"{self.api.current_league}&type=Currency&language=en"
        )
        currency_prices: Dict[str, float] = {}

        response = requests.get(url).json()
        for currency in response["lines"]:
            currency_prices[currency["currencyTypeName"]] = currency["chaosEquivalent"]

        return currency_prices
