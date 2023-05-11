from typing import Any, Dict

from gems.builder import Builder
from gems.gem import Gem


class GemBuilder(Builder):
    def __init__(self, gem_data: Dict[str, Dict[str, Any]]):
        self.gem_data = gem_data
        self.__gem: Gem = None
        self.vaal_name: str = ""
        self.quality: str = ""

    @staticmethod
    def __get_quality(name: str) -> str:
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

    @staticmethod
    def __get_vaal_name(name: str) -> str:
        for quality_type in ["Anomalous", "Divergent", "Phantasmal"]:
            if quality_type in name:
                split_name = name.split()
                split_name.insert(1, "Vaal")
                name = " ".join(split_name)
                return name

        return "Vaal " + name

    def __get_gem_price(self, name: str, suffix: str) -> float:
        gem_name_with_suffix = f"{name}|{suffix}"

        if gem_name_with_suffix in self.gem_data:
            price = self.gem_data[gem_name_with_suffix]["chaosValue"]
            return price

        price = 0
        return price

    def __get_gem_listings_count(self, name: str, suffix: str) -> int:
        gem_name_with_suffix = f"{name}|{suffix}"

        if gem_name_with_suffix in self.gem_data:
            count = self.gem_data[gem_name_with_suffix]["listingCount"]
            return count

        count = 0
        return count

    def set_name(self, name: str) -> Builder:
        name = name.split("|")[0]

        if "Vaal" in name:
            name = name.replace("Vaal ", "")

        self.vaal_name = self.__get_vaal_name(name)
        self.quality = self.__get_quality(name)
        self.__gem.name = name
        return self

    def set_buy_price(self) -> Builder:
        if self.quality == "Basic":
            self.__gem.buy_price = self.__get_gem_price(self.__gem.name, "1/20")
            return self

        self.__gem.buy_price = self.__get_gem_price(self.__gem.name, "1")
        return self

    def set_fail_price(self) -> Builder:
        if self.quality == "Awakened":
            self.__gem.fail_price = self.__get_gem_price(self.__gem.name, "5/20c")
            return self

        self.__gem.fail_price = self.__get_gem_price(self.__gem.name, "20/20c")
        return self

    def set_vaal_price(self) -> Builder:
        self.__gem.vaal_price = self.__get_gem_price(self.vaal_name, "20/20c")
        return self

    def set_success_price(self) -> Builder:
        if self.quality == "Awakened":
            self.__gem.success_price = self.__get_gem_price(self.__gem.name, "6/20c")
            return self

        self.__gem.success_price = self.__get_gem_price(self.__gem.name, "21/20c")
        return self

    def set_listed_successful(self) -> Builder:
        if self.quality == "Awakened":
            self.__gem.listed_successful = self.__get_gem_listings_count(
                self.__gem.name, "6/20c"
            )
            return self

        self.__gem.listed_successful = self.__get_gem_listings_count(
            self.__gem.name, "21/20c"
        )
        return self

    def set_leveled_price(self) -> Builder:
        if self.quality == "Awakened":
            self.__gem.leveled_price = self.__get_gem_price(self.__gem.name, "5/20")
            return self

        self.__gem.leveled_price = self.__get_gem_price(self.__gem.name, "20/20")
        return self

    def set_listed_leveled(self) -> Builder:
        if self.quality == "Awakened":
            self.__gem.listed_leveled = self.__get_gem_listings_count(
                self.__gem.name, "5/20"
            )
            return self

        self.__gem.listed_leveled = self.__get_gem_listings_count(
            self.__gem.name, "20/20"
        )
        return self

    def build_corrupted_gem(self, name: str, gem_type: Gem) -> Gem:
        self.__gem = gem_type

        self.set_name(name)\
            .set_buy_price()\
            .set_fail_price()\
            .set_success_price()\
            .set_listed_successful()\
            .set_vaal_price()

        return self.__gem

    def build_leveled_gem(self, name: str, gem_type: Gem) -> Gem:
        self.__gem = gem_type

        self.set_name(name)\
            .set_buy_price()\
            .set_leveled_price()\
            .set_listed_leveled()

        return self.__gem
