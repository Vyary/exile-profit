import json
from typing import Dict

from boss_check.boss_check import BossChecker
from currency_exchange.currency_exchange import CurrencyExchange
from divination_cards.div_card_creator import DivCardCreator
from gems.gem_builder import GemBuilder
from gems.gem_builder_manager import GemBuildManager
from gs_manager.google_sheet_manager import SheetUpdater
from items.basic_item import BasicItem
from items.divination_card import DivCard
from limiter.poe_trade_limiter import PoeTradeLimiter
from poe_ninja.poe_ninja import CurrencyPrices, MassiveData, PoeNinjaAPI, SkillGems
from poe_trade.poe_trade import (
    CurrencyAliasesProvider,
    ItemFetcher,
    League,
    PoeTrade,
    TradeSearcher,
)
from save_data.save_data import SaveData
from storages.item_storage import ItemStorage


class Controller:
    def update_gems(
        self,
        gem_builder: GemBuilder,
        gem_manager: GemBuildManager,
        storage: ItemStorage,
        save_manager: SaveData,
        sheet: SheetUpdater,
    ):
        with open("src/queries/gem_queries.json", "r") as file:
            gem_queries = json.load(file)

        corrupted_gem_repository, leveled_gem_repository = gem_manager.gem_info(
            gem_queries, gem_builder, storage
        )

        save_manager.save_dict_to_csv(
            "gems_to_corrupt.csv", corrupted_gem_repository, "success_price"
        )
        sheet.update("Gems to Corrupt", "output/gems_to_corrupt.csv")

        save_manager.save_dict_to_csv(
            "gems_to_level.csv", leveled_gem_repository, "profit"
        )
        sheet.update("Gems to Level", "output/gems_to_level.csv")

    def update_divination_cards(
        self,
        div_card_creator: DivCardCreator,
        save_manager: SaveData,
        sheet: SheetUpdater,
    ):
        with open("src/queries/divination_cards_queries.json", "r") as f:
            divination_cards_queries = json.load(f)

        div_info = div_card_creator.div_cards_info(divination_cards_queries)
        save_manager.save_dict_to_csv("div_info.csv", div_info, "profit")
        sheet.update("Divination Cards", "output/div_info.csv")

    def update_twisted_invitation(
        self, boss_check: BossChecker, save_manager: SaveData, sheet: SheetUpdater
    ):
        with open("src/queries/twisted_invitation.json", "r") as file:
            twisted_invitation = json.load(file)

        twisted_invitation_info = boss_check.get_boss_info(twisted_invitation)
        save_manager.save_dict_to_csv("twisted_invitation.csv", twisted_invitation_info)
        sheet.update("Twisted Invitation", "output/twisted_invitation.csv.")

    def update_uber_maven(
        self, boss_check: BossChecker, save_manager: SaveData, sheet: SheetUpdater
    ):
        with open("src/queries/uber_maven_queries.json", "r") as file:
            uber_maven_queries = json.load(file)

        uber_maven_info = boss_check.get_boss_info(uber_maven_queries)
        save_manager.save_dict_to_csv("uber_maven_info.csv", uber_maven_info)
        sheet.update("Uber Maven", "output/uber_maven_info.csv.")

    def update_uber_sirus(
        self, boss_check: BossChecker, save_manager: SaveData, sheet: SheetUpdater
    ):
        with open("src/queries/uber_sirus_queries.json", "r") as file:
            uber_sirus_queries = json.load(file)

        uber_sirus_info = boss_check.get_boss_info(uber_sirus_queries)
        save_manager.save_dict_to_csv("uber_sirus_info.csv", uber_sirus_info)
        sheet.update("Uber Sirus", "output/uber_sirus_info.csv.")

    def update_currency_flipping(
        self,
        currency_prices: Dict[str, float],
        save_manager: SaveData,
        sheet: SheetUpdater,
    ):
        with open("src/queries/exchangeable_currencies.json") as f:
            exchangeable_currencies = json.load(f)

        currency_exchange_data = CurrencyExchange.get_exchange_currency_data(
            exchangeable_currencies, currency_prices
        )
        save_manager.save_dict_to_csv(
            "currency_exchange.csv", currency_exchange_data, "profit_per_100"
        )
        sheet.update("Currency Flipping", "output/currency_exchange.csv")

    def run(self):
        current_league = League().current()

        poe_trade_limiter = PoeTradeLimiter()
        trade_searcher = TradeSearcher()
        item_fetcher = ItemFetcher()
        currency_aliases = CurrencyAliasesProvider()

        poe_ninja_api = PoeNinjaAPI(current_league)
        massive_data = MassiveData(poe_ninja_api).get_massive_data()
        gem_data = SkillGems(poe_ninja_api).get_gems_data()
        currency_prices = CurrencyPrices(poe_ninja_api).get_currency_prices()
        gem_manager = GemBuildManager()

        save_manager = SaveData()
        storage = ItemStorage()
        sheet = SheetUpdater("output/service_account.json", "Exile-Profit")

        item_creator = BasicItem()
        items_cache = {}

        price_checker = PoeTrade(
            current_league,
            poe_trade_limiter,
            massive_data,
            trade_searcher,
            item_fetcher,
            currency_aliases,
        )

        div_item_class = DivCard()
        div_card_creator = DivCardCreator(
            current_league,
            massive_data,
            price_checker,
            div_item_class,
            items_cache,
            storage,
        )

        gem_builder = GemBuilder(current_league, price_checker, gem_data)
        boss_check = BossChecker(
            massive_data,
            price_checker,
            items_cache,
            save_manager,
            sheet,
            storage,
            item_creator,
        )

        # Update Divination Cards
        self.update_divination_cards(div_card_creator, save_manager, sheet)
        # Update Gems
        self.update_gems(gem_builder, gem_manager, storage, save_manager, sheet)
        # Update Bosses
        self.update_uber_sirus(boss_check, save_manager, sheet)
        self.update_uber_maven(boss_check, save_manager, sheet)
        self.update_twisted_invitation(boss_check, save_manager, sheet)
        # Update Currency Flipping
        self.update_currency_flipping(currency_prices, save_manager, sheet)


def main():
    controller = Controller()
    controller.run()


if __name__ == "__main__":
    main()
