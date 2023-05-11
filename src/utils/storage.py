from typing import Any, Dict


class Storage:
    def __init__(self):
        self.inventory: Dict[str, Any] = {}

    def add_item(self, item: Any):
        self.inventory[item.name] = item
