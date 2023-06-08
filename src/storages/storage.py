from abc import ABC, abstractmethod
from typing import Dict

from items.item import Item


class Storage(ABC):
    def __init__(self):
        self.inventory: Dict[str, Item] = {}

    @abstractmethod
    def add_item(self, item: Item):
        pass
