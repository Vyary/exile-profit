from typing import Any, Dict

from gems.builder import Builder
from gems.gem import Gem


class GemBuilder(Builder):
    def __init__(self, current_league: str, gem_data: Dict[str, Dict[str, Any]]):
        self.current_league = current_league
        self.gem_data = gem_data
        self.__gem: Gem = None
        self.vaal_name: str = ""
        self.quality: str = ""

    @staticmethod
    def __get_quality(name: str) -> str:
        quality_types = {
            "Vaal": ["Vaal"],
            "Anomalous": ["Anomalous"],
            "Divergent": ["Divergent"],
            "Phantasmal": ["Phantasmal"],
            "Awakened": ["Awakened"],
            "Exceptional": ["Enlighten", "Enhance", "Empower"],
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

        return 0

    def __get_gem_listings_count(self, name: str, suffix: str) -> int:
        gem_name_with_suffix = f"{name}|{suffix}"

        if gem_name_with_suffix in self.gem_data:
            count = self.gem_data[gem_name_with_suffix]["listingCount"]
            return count

        return 0

    def set_name(self, name: str) -> Builder:
        name = name.split("|")[0]

        if "Vaal" in name:
            name = name.replace("Vaal ", "")

        self.vaal_name = self.__get_vaal_name(name)
        self.quality = self.__get_quality(name)
        self.__gem.name = name
        return self

    def set_buy_price(self) -> Builder:
        variant = "1"

        if self.quality == "Basic":
            variant = "1/20"

        self.__gem.buy_price = self.__get_gem_price(self.__gem.name, variant)
        return self

    def set_fail_price(self) -> Builder:
        variant = "20/20c"

        if self.quality == "Awakened":
            variant = "5/20c"

        if self.quality == "Exceptional":
            variant = "3c"

        self.__gem.fail_price = self.__get_gem_price(self.__gem.name, variant)
        return self

    def set_vaal_price(self) -> Builder:
        self.__gem.vaal_price = self.__get_gem_price(self.vaal_name, "20/20c")
        return self

    def set_success_price(self) -> Builder:
        variant = "21/20c"

        if self.quality == "Awakened":
            variant = "6/20c"

        if self.quality == "Exceptional":
            variant = "4c"

        self.__gem.success_price = self.__get_gem_price(self.__gem.name, variant)
        return self

    def set_listed_successful(self) -> Builder:
        variant = "21/20c"

        if self.quality == "Awakened":
            variant = "6/20c"

        if self.quality == "Exceptional":
            variant = "4c"

        self.__gem.listed_successful = self.__get_gem_listings_count(
            self.__gem.name, variant
        )
        return self

    def set_leveled_price(self) -> Builder:
        variant = "20/20"

        if self.quality == "Awakened":
            variant = "5/20"

        if self.quality == "Exceptional":
            variant = "3"

        self.__gem.leveled_price = self.__get_gem_price(self.__gem.name, variant)
        return self

    def set_listed_leveled(self) -> Builder:
        variant = "20/20"

        if self.quality == "Awakened":
            variant = "5/20"

        if self.quality == "Exceptional":
            variant = "3"

        self.__gem.listed_leveled = self.__get_gem_listings_count(
            self.__gem.name, variant
        )
        return self

    def set_leveled_profit(self) -> Builder:
        self.__gem.profit = self.__gem.leveled_price - self.__gem.buy_price
        return self

    def __get_trade_link_query(self, name_for_link: str, gem_quality: str) -> str:
        if gem_quality == "Anomalous":
            return f'{{%22query%22:{{%22filters%22:{{%22misc_filters%22:{{%22filters%22:{{%22gem_level%22:{{%22min%22:1,%22max%22:20}},%22corrupted%22:{{%22option%22:false}},%22gem_alternate_quality%22:{{%22option%22:%221%22}},%22quality%22:{{}}}}}}}},%22type%22:%22{name_for_link}%22}}}}'

        if gem_quality == "Divergent":
            return f'{{%22query%22:{{%22filters%22:{{%22misc_filters%22:{{%22filters%22:{{%22gem_level%22:{{%22min%22:1,%22max%22:20}},%22corrupted%22:{{%22option%22:false}},%22gem_alternate_quality%22:{{%22option%22:%222%22}},%22quality%22:{{}}}}}}}},%22type%22:%22{name_for_link}%22}}}}'

        if gem_quality == "Phantasmal":
            return f'{{%22query%22:{{%22filters%22:{{%22misc_filters%22:{{%22filters%22:{{%22gem_level%22:{{%22min%22:1,%22max%22:20}},%22corrupted%22:{{%22option%22:false}},%22gem_alternate_quality%22:{{%22option%22:%223%22}},%22quality%22:{{}}}}}}}},%22type%22:%22{name_for_link}%22}}}}'

        return f'{{%22query%22:{{%22filters%22:{{%22misc_filters%22:{{%22filters%22:{{%22gem_level%22:{{%22min%22:1,%22max%22:20}},%22corrupted%22:{{%22option%22:false}},%22quality%22:{{}}}}}}}},%22type%22:%22{name_for_link}%22}}}}'

    def create_trade_link(self) -> Builder:
        gem_name = self.__gem.name
        gem_quality = self.quality

        if gem_quality != "Awakened" and gem_quality != "Basic":
            gem_name = gem_name.replace(gem_quality, "").strip()

        name_for_link = gem_name.replace(" ", "%20")
        query = self.__get_trade_link_query(name_for_link, gem_quality)

        trade_link = f'=HYPERLINK("https://www.pathofexile.com/trade/search/{self.current_league}?q={query}","Trade")'
        self.__gem.trade_link = trade_link
        return self

    def build_corrupted_gem(self, name: str, gem_type: Gem) -> Gem:
        self.__gem = gem_type

        self.set_name(name)\
            .set_buy_price()\
            .set_fail_price()\
            .set_success_price()\
            .set_listed_successful()\
            .set_vaal_price()\
            .create_trade_link()

        return self.__gem

    def build_leveled_gem(self, name: str, gem_type: Gem) -> Gem:
        self.__gem = gem_type

        self.set_name(name)\
            .set_buy_price()\
            .set_leveled_price()\
            .set_listed_leveled()\
            .set_leveled_profit()\
            .create_trade_link()

        return self.__gem
