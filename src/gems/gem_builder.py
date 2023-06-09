from typing import Any, Dict, Tuple

from items.corrupted_gem import CorruptedGem
from items.leveled_gem import LeveledGem
from poe_trade.poe_trade import PoeTrade


class GemBuilder:
    def __init__(
        self,
        current_league: str,
        price_checker: PoeTrade,
        gem_data: Dict[str, Dict[str, Any]],
    ):
        self.current_league = current_league
        self.price_checker = price_checker
        self.gem_data = gem_data
        self.__gem: LeveledGem | CorruptedGem = None
        self.__total_listed: int = 0

    def get_price(self, name: str, query: Dict[str, Any]) -> float:
        if name in self.gem_data:
            price = self.gem_data[name]["chaosValue"]
            return price

        return 0
        gem_info = self.price_checker.get_item_price(query)
        price = gem_info[0]

        if name.endswith(("20/20", "5/20", "4/20", "3")):
            self.__total_listed = gem_info[1]

        if name.endswith(("21/20c", "6/20c", "5/20c", "4c")):
            self.__total_listed = gem_info[1]

        return price

    def set_name(self, gem_name: str) -> "GemBuilder":
        self.__gem.name = gem_name
        return self

    def set_buy_price(self, buy_name: str, query: Dict[str, Any]) -> "GemBuilder":
        self.__gem.buy_price = self.get_price(buy_name, query)
        return self

    def set_fail_price(self, fail_name: str, query: Dict[str, Any]) -> "GemBuilder":
        self.__gem.fail_price = self.get_price(fail_name, query)
        return self

    def set_success_price(
        self, success_name: str, query: Dict[str, Any]
    ) -> "GemBuilder":
        self.__gem.success_price = self.get_price(success_name, query)
        return self

    def set_listed_successful(self, success_name: str):
        if success_name in self.gem_data:
            self.__gem.listed_leveled = self.gem_data[success_name]["listingCount"]
            return self

        self.__gem.listed_leveled = self.__total_listed
        return self

    def set_vaal_price(self, vaal_name: str, query: Dict[str, Any]) -> "GemBuilder":
        if vaal_name is None:
            self.__gem.vaal_price = 0
            return self

        self.__gem.vaal_price = self.get_price(vaal_name, query)
        return self

    def set_leveled_price(
        self, leveled_name: str, query: Dict[str, Any]
    ) -> "GemBuilder":
        self.__gem.leveled_price = self.get_price(leveled_name, query)
        return self

    def set_listed_leveled(self, leveled_name: str):
        if leveled_name in self.gem_data:
            self.__gem.listed_leveled = self.gem_data[leveled_name]["listingCount"]
            return self

        self.__gem.listed_leveled = self.__total_listed
        return self

    def set_leveled_profit(self) -> "GemBuilder":
        self.__gem.profit = self.__gem.leveled_price - self.__gem.buy_price
        return self

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

    def __get_trade_link_query(self, name_for_link: str, gem_quality: str) -> str:
        if gem_quality == "Anomalous":
            return f"{{%22query%22:{{%22filters%22:{{%22misc_filters%22:{{%22filters%22:{{%22gem_level%22:{{%22min%22:1,%22max%22:20}},%22corrupted%22:{{%22option%22:false}},%22gem_alternate_quality%22:{{%22option%22:%221%22}},%22quality%22:{{}}}}}}}},%22type%22:%22{name_for_link}%22}}}}"

        if gem_quality == "Divergent":
            return f"{{%22query%22:{{%22filters%22:{{%22misc_filters%22:{{%22filters%22:{{%22gem_level%22:{{%22min%22:1,%22max%22:20}},%22corrupted%22:{{%22option%22:false}},%22gem_alternate_quality%22:{{%22option%22:%222%22}},%22quality%22:{{}}}}}}}},%22type%22:%22{name_for_link}%22}}}}"

        if gem_quality == "Phantasmal":
            return f"{{%22query%22:{{%22filters%22:{{%22misc_filters%22:{{%22filters%22:{{%22gem_level%22:{{%22min%22:1,%22max%22:20}},%22corrupted%22:{{%22option%22:false}},%22gem_alternate_quality%22:{{%22option%22:%223%22}},%22quality%22:{{}}}}}}}},%22type%22:%22{name_for_link}%22}}}}"

        return f"{{%22query%22:{{%22filters%22:{{%22misc_filters%22:{{%22filters%22:{{%22gem_level%22:{{%22min%22:1,%22max%22:20}},%22corrupted%22:{{%22option%22:false}},%22quality%22:{{}}}}}}}},%22type%22:%22{name_for_link}%22}}}}"

    def create_trade_link(self) -> "GemBuilder":
        gem_name = self.__gem.name
        gem_quality = self.__get_quality(gem_name)

        if gem_quality != "Awakened" and gem_quality != "Basic":
            gem_name = gem_name.replace(gem_quality, "").strip()

        name_for_link = gem_name.replace(" ", "%20")
        query = self.__get_trade_link_query(name_for_link, gem_quality)

        trade_link = f'=HYPERLINK("https://www.pathofexile.com/trade/search/{self.current_league}?q={query}","Trade")'
        self.__gem.trade_link = trade_link
        return self

    def build_corrupted_gem(
        self,
        gem_type: CorruptedGem,
        gem_name: str,
        buy: Tuple[str, Dict[str, Any]],
        fail: Tuple[str, Dict[str, Any]],
        success: Tuple[str, Dict[str, Any]],
        vaal: Tuple[str, Dict[str, Any]],
    ) -> CorruptedGem:
        self.__gem = gem_type

        self.set_name(gem_name).set_buy_price(*buy).set_fail_price(
            *fail
        ).set_success_price(*success).set_listed_successful(success[0]).set_vaal_price(
            *vaal
        ).create_trade_link()

        return self.__gem

    def build_leveled_gem(
        self,
        gem_type: LeveledGem,
        gem_name: str,
        buy: Tuple[str, Dict[str, Any]],
        leveled: Tuple[str, Dict[str, Any]],
    ) -> LeveledGem:
        self.__gem = gem_type

        self.set_name(gem_name).set_buy_price(*buy).set_leveled_price(
            *leveled
        ).set_listed_leveled(leveled[0]).set_leveled_profit().create_trade_link()

        return self.__gem
