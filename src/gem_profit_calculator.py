from typing import Dict

import pandas as pd
import requests

from get_league import current_league


class Gem:
    dictionary: Dict[str, "Gem"] = {}

    def __init__(self, name: str) -> None:
        self.name: str = name
        self.quality: str = self.get_quality_type(name)
        self.base_price: float = 0
        self.leveled_price: float = 0
        self.fail_price: float = 0
        self.success_price: float = 0
        self.vaal_price: float = 0
        self.listed_leveled: int = 0
        self.listed_21_20: int = 0

    @staticmethod
    def get_quality_type(name: str) -> str:
        quality_types = {
            "Vaal": ["Vaal"],
            "Alternative": ["Anomalous", "Divergent", "Phantasmal"],
            "Awakened": ["Awakened"],
        }

        for quality, prefixes in quality_types.items():
            for prefix in prefixes:
                if prefix in name:
                    return quality

        return "Basic"

    def update_prices(self, variant: str, quality: str, price: float, listed: int):
        # base price
        is_basic_1_20 = variant == "1/20" and quality == "Basic"
        is_alternative_1 = variant == "1" and quality == "Alternative"
        is_awakened_1 = variant == "1" and quality == "Awakened"
        # leveled price
        is_leveled_20_20 = variant == "20/20"
        # fail price
        is_not_vaal_20_20c = variant == "20/20c" and quality != "Vaal"
        is_awakened_5_20c = variant == "5/20c" and quality == "Awakened"
        # semi fail price
        is_vaal_20_20c = variant == "20/20c" and quality == "Vaal"
        # success price
        is_not_vaal_21_20c = variant == "21/20c" and quality != "Vaal"
        is_awakened_6_20c = variant == "6/20c" and quality == "Awakened"

        if is_basic_1_20 or is_alternative_1 or is_awakened_1:
            self.base_price = price
        elif is_leveled_20_20:
            self.leveled_price = price
            self.listed_leveled = listed
        elif is_not_vaal_20_20c or is_awakened_5_20c:
            self.fail_price = price
        elif is_vaal_20_20c:
            self.vaal_price = price
        elif is_not_vaal_21_20c or is_awakened_6_20c:
            self.success_price = price
            self.listed_21_20 = listed

    @classmethod
    def rehearse_response(cls, data: dict) -> None:
        for gem in data["lines"]:
            gem_name = gem["name"]
            variant = gem["variant"]
            price = gem["chaosValue"]
            listed = gem.get("listingCount", 0)

            quality = cls.get_quality_type(gem_name)

            if quality == "Vaal":
                gem_name = gem_name.replace("Vaal ", "")

            if gem_name not in cls.dictionary:
                cls.dictionary[gem_name] = cls(gem_name)

            cls.dictionary[gem_name].update_prices(variant, quality, price, listed)

    @classmethod
    def save_data(cls) -> None:
        data = [
            {
                "Gem Name": gem.name,
                "Buy price": gem.base_price,
                "Corrupted 20/20": gem.fail_price,
                "Success 21/20": gem.success_price,
                "Listed 21/20": gem.listed_21_20,
                "Vaal price": gem.vaal_price,
                "Leveled 20/20": gem.leveled_price,
                "Listed L20/20": gem.listed_leveled,
            }
            for gem in Gem.dictionary.values()
        ]

        df = pd.DataFrame(data)

        df.columns = [
            "Gem Name",
            "Buy price",
            "Corrupted 20/20",
            "Success 21/20",
            "Listed 21/20",
            "Vaal price",
            "Leveled 20/20",
            "Listed L20/20",
        ]

        df1 = df[
            [
                "Gem Name",
                "Buy price",
                "Corrupted 20/20",
                "Success 21/20",
                "Listed 21/20",
                "Vaal price",
            ]
        ]

        df2 = df[
            [
                "Gem Name",
                "Buy price",
                "Leveled 20/20",
                "Listed L20/20",
            ]
        ]

        df1 = df1.sort_values("Success 21/20", ascending=False)
        df1.to_csv("output/gems_to_corrupt.csv", index=False, encoding="utf-8")

        df2 = df2.sort_values("Leveled 20/20", ascending=False)
        df2.to_csv("output/gems_to_level.csv", index=False, encoding="utf-8")


def main():
    league = current_league()

    if league.startswith("Error"):
        exit()

    url = (
        f"https://poe.ninja/api/data/itemoverview?league={league}"
        "&type=SkillGem&language=en"
    )

    response = requests.get(url).json()

    Gem.rehearse_response(response)
    Gem.save_data()


if __name__ == "__main__":
    main()
