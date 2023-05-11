from abc import ABC, abstractmethod
from typing import Any, Dict


class APICall(ABC):
    @abstractmethod
    def __init__(self):
        pass

    def get_price(self, query: Dict[str, Any]) -> float:
        return 0.0
