from abc import ABC, abstractmethod


class Gem(ABC):
    @abstractmethod
    def __init__(self):
        self.name: str = ""
        self.buy_price: float = 0
        self.fail_price: float = 0
        self.success_price: float = 0
        self.listed_successful: int = 0
        self.vaal_price: float = 0
        self.leveled_price: float = 0
        self.listed_leveled: int = 0
        self.profit: float = 0
        self.trade_link: str = ""
