from typing import Any, Dict, List

from tqdm import tqdm

from gs_manager.google_sheet_manager import SheetUpdater
from items.basic_item import BasicItem
from poe_trade.poe_trade import PoeTrade
from save_data.save_data import SaveData
from storages.item_storage import ItemStorage


class BossChecker:
    def __init__(
        self,
        massive_data: Dict[str, Any],
        price_checker: PoeTrade,
        items_cache: Dict[str, Any],
        save_manager: SaveData,
        sheet_updater: SheetUpdater,
        storage: ItemStorage,
        item_creator: BasicItem,
    ):
        self.massive_data = massive_data
        self.price_checker = price_checker
        self.items_cache = items_cache
        self.save_manager = save_manager
        self.sheet_updater = sheet_updater
        self.storage = storage
        self.item_creator = item_creator

    def __get_item_price(self, item: str, query: Dict[str, Any]) -> float:
        if item in self.massive_data:
            return float(self.massive_data[item]["chaos"])

        if item in self.items_cache:
            return self.items_cache[item]

        item_price = self.price_checker.get_item_price(query)[0]

        if item not in self.items_cache:
            self.items_cache[item] = item_price

        return float(item_price)

    def get_boss_info(self, boss_queries: Dict[str, Any]):
        boss_drops = self.storage.new_storage()

        for item, values in tqdm(boss_queries.items(), desc="Boss Info"):
            prices: List[float] = []

            for component, query in values["components"].items():
                prices.append(self.__get_item_price(component, query))

            average_price = sum(prices) / len(prices)

            current_item = self.item_creator.create_item(
                item, values["drop_chance"], average_price
            )
            boss_drops.add_item(current_item)

        return boss_drops.inventory
