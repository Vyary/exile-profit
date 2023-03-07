import json
from typing import Dict

import pandas as pd
import requests

from get_league import current_league


def get_currency_data(league: str) -> Dict:
    url = (
        f"https://poe.ninja/api/data/currencyoverview?league="
        f"{league}&type=Currency&language=en"
    )
    response = requests.get(url).json()
    return response


def set_currency_price(currency_data: Dict, currency_dictionary: Dict) -> None:
    for element in currency_data["lines"]:
        for currency in currency_dictionary:
            if element["currencyTypeName"] == currency:
                currency_dictionary[currency]["currency_value"] = element["receive"][
                    "value"
                ]
                break


def set_exchange_rate(currency_dictionary: Dict) -> None:
    for currency in currency_dictionary:
        exchanges_for = currency_dictionary[currency]["exchange_for"]
        exchange_currency_price = currency_dictionary[exchanges_for]["currency_value"]
        currency_dictionary[currency][
            "exchange_currency_price"
        ] = exchange_currency_price


def calculate_profit(currency_dictionary: Dict) -> None:
    for currency in currency_dictionary:
        currency_value = currency_dictionary[currency]["currency_value"]
        exchange_currency_price = currency_dictionary[currency][
            "exchange_currency_price"
        ]
        exchange_rate = currency_dictionary[currency]["exchange_rate"]

        profit = (currency_value - exchange_rate * exchange_currency_price) * 100
        currency_dictionary[currency]["profit"] = float(f"{profit:.2f}")


def save_data(currency_dictionary: Dict) -> None:
    df = pd.DataFrame.from_dict(currency_dictionary, orient="index")
    df = df.sort_values("profit", ascending=False)
    df.index.name = "Currency"
    df.columns = [
        "Price",
        "Component",
        "Count",
        "Component Price",
        "Profit per 100",
    ]
    df.to_csv("output/currency_exchange.csv", encoding="utf-8")


def main():
    with open("src/currency_data.json") as f:
        currency_dictionary = json.load(f)

    currency_data = get_currency_data(current_league())
    set_currency_price(currency_data, currency_dictionary)
    set_exchange_rate(currency_dictionary)
    calculate_profit(currency_dictionary)
    save_data(currency_dictionary)


if __name__ == "__main__":
    main()
