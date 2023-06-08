from typing import Dict

from items.item import Item
from storages.storage import Storage


class ItemStorage(Storage):
    def __init__(self):
        self.inventory: Dict[str, Item] = {}

    def add_item(self, item: Item):
        self.inventory[item.name] = item

    @classmethod
    def new_storage(cls):
        return ItemStorage()
