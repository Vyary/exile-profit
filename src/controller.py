import json
from typing import Any, Dict

from boss_drop_info.boss_drop_info import BossDropInfo
from boss_drop_info.item import Item
from currency_exchange.currency_exchange import CurrencyExchange
from divination_cards.combined_divination_card_creator import CombinedDivCardCreator
from divination_cards.div_card import DivCard
from gems.corrupted_gem import CorruptedGem
from gems.gem_builder import GemBuilder
from gems.gem_repository import GemRepository
from gems.leveled_gem import LeveledGem
from utils.currency_prices import CurrencyPrices
from utils.current_league import League
from utils.google_sheet_manager import SheetUpdater
from utils.limiter.rate_limiter import RateLimiter
from utils.price_check.api_call import APICall
from utils.price_check.poe_ninja import PoeNinja
from utils.price_check.poe_trade import PoeTrade
from utils.save_data.save_data import SaveData
from utils.storage import Storage


class Controller:
    def create_gem_repository(self, gems_data: Dict[str, Any]):
        corrupted_gem_repository = GemRepository()
        leveled_gem_repository = GemRepository()

        builder = GemBuilder(gems_data)

        for gem_name in gems_data:
            corrupted_gem = builder.build_corrupted_gem(gem_name, CorruptedGem())
            leveled_gem = builder.build_leveled_gem(gem_name, LeveledGem())

            if corrupted_gem.name not in corrupted_gem_repository.gems:
                corrupted_gem_repository.add_gem(corrupted_gem)

            if leveled_gem.name not in leveled_gem_repository.gems:
                leveled_gem_repository.add_gem(leveled_gem)

        return corrupted_gem_repository.gems, leveled_gem_repository.gems

    def uber_sirus_info(
        self,
        boss_checker: BossDropInfo,
        cached_storage: Dict[str, Item] = None,
    ) -> Dict[str, Item]:
        with open("src/boss_drop_info/boss_queries/uber_sirus_queries.json") as f:
            # Load the JSON data into a dictionary
            uber_sirus_queries = json.load(f)

        uber_sirus_item_storage = Storage()
        uber_sirus_info = boss_checker.get_items_prices(
            uber_sirus_queries, uber_sirus_item_storage, cached_storage
        )

        return uber_sirus_info

    def uber_maven_info(
        self,
        boss_checker: BossDropInfo,
        cached_storage: Dict[str, Item] = None,
    ) -> Dict[str, Item]:
        with open("src/boss_drop_info/boss_queries/uber_maven_queries.json") as f:
            # Load the JSON data into a dictionary
            uber_maven_queries = json.load(f)

        uber_maven_item_storage = Storage()
        uber_maven_info = boss_checker.get_items_prices(
            uber_maven_queries, uber_maven_item_storage, cached_storage
        )

        return uber_maven_info

    def divination_cards_data(
        self,
        poe_ninja_api: PoeNinja,
        price_check_method: APICall,
        massive_data_without_types: Dict[str, Any],
    ):
        divination_cards_data = poe_ninja_api.get_divination_cards_data()
        div_class = DivCard()
        divination_card_storage = Storage()

        with open(
            "src/divination_cards/divination_cards_queries/divination_cards_queries.json"
        ) as f:
            # Load the JSON data into a dictionary
            divination_cards_queries = json.load(f)

        complete_div_cards = CombinedDivCardCreator(
            divination_cards_data,
            massive_data_without_types,
            divination_cards_queries,
            price_check_method,
            div_class,
            divination_card_storage,
        ).create_div_card()

        return complete_div_cards

    def run(self):
        current_league = League().current_league()
        poe_ninja_api = PoeNinja(current_league)
        limiter = RateLimiter()
        save_manager = SaveData()
        currency_prices = CurrencyPrices(current_league).get_currency_prices()
        price_check_method = PoeTrade(current_league, currency_prices, limiter)
        sheet = SheetUpdater("output/service_account.json", "Exile-Profit")
        untyped_data_dict = poe_ninja_api.get_massive_data()
        item_maker = Item()
        boss_checker = BossDropInfo(price_check_method, item_maker, untyped_data_dict)
        currency_exchange = CurrencyExchange()

        # Gems
        gems_data = poe_ninja_api.get_gems_data()
        corrupted_gems, leveled_gem_repository = self.create_gem_repository(gems_data)
        save_manager.save_dict_to_csv(
            "gems_to_corrupt.csv", corrupted_gems, "success_price"
        )
        sheet.update("Gems to Corrupt", "output/gems_to_corrupt.csv")

        save_manager.save_dict_to_csv(
            "gems_to_level.csv", leveled_gem_repository, "leveled_price"
        )
        sheet.update("Gems to Level", "output/gems_to_level.csv")

        # Currency Flipping
        with open("src/currency_exchange/exchangeable_currencies.json") as f:
            # Load the JSON data into a dictionary
            exchangeable_currencies = json.load(f)

        currency_exchange_data = currency_exchange.get_exchange_currency_data(
            exchangeable_currencies, currency_prices
        )
        save_manager.save_dict_to_csv(
            "currency_exchange.csv", currency_exchange_data, "profit_per_100"
        )
        sheet.update("Currency Flipping", "output/currency_exchange.csv")

        # Div Cards
        div_cards_info = self.divination_cards_data(
            poe_ninja_api, price_check_method, untyped_data_dict
        )
        save_manager.save_dict_to_csv("div_cards.csv", div_cards_info, "profit")
        sheet.update("Divination Cards", "output/div_cards.csv")

        # Uber Sirus
        uber_sirus_info = self.uber_sirus_info(boss_checker)
        save_manager.save_dict_to_csv("uber_sirus_info.csv", uber_sirus_info)
        sheet.update("Uber Sirus", "output/uber_sirus_info.csv")

        # Uber Maven
        uber_maven_info = self.uber_maven_info(boss_checker)
        save_manager.save_dict_to_csv("uber_maven_info.csv", uber_maven_info)
        sheet.update("Uber Maven", "output/uber_maven_info.csv")


def main():
    controller = Controller()
    controller.run()


if __name__ == "__main__":
    main()
