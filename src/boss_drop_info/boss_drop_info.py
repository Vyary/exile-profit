from typing import Any, Dict

from boss_drop_info.item import Item
from utils.price_check.api_call import APICall
from utils.storage import Storage


class BossDropInfo:
    def __init__(
        self,
        price_check_method: APICall,
        item_maker: Item,
        untyped_data_dict: Dict[str, Any] = None,
    ):
        self.price_check_method = price_check_method
        self.item_maker = item_maker
        self.untyped_data_dict = untyped_data_dict

    def get_items_prices(
        self,
        item_queries: Dict[str, Any],
        storage: Storage,
        cached_storage: Dict[str, Item] = None,
    ) -> Dict[str, Item]:
        for item_name, values in item_queries.items():
            item_drop_chance = values["drop_chance"]

            if self.untyped_data_dict and item_name in self.untyped_data_dict:
                item_price = self.untyped_data_dict[item_name]["chaos"]
            elif cached_storage and item_name in cached_storage:
                item_price = cached_storage[item_name].price
            else:
                item_price = self.price_check_method.get_price(values["query"])

            new_item = self.item_maker.create_item(
                item_name, item_drop_chance, item_price
            )
            storage.add_item(new_item)

        return storage.inventory
