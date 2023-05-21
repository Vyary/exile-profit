from abc import ABC, abstractmethod
from typing import Any, Dict


class DivCardCreator(ABC):
    @abstractmethod
    def create_div_cards(self) -> Dict[str, Any]:
        pass
