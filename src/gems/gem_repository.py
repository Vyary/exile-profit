from typing import Dict

from gems.gem import Gem


class GemRepository:
    def __init__(self):
        self.gems: Dict[str, Gem] = {}

    def add_gem(self, gem: Gem):
        self.gems[gem.name] = gem

    def get_gem(self, name: str):
        return self.gems.get(name)
