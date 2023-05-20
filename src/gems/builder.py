from abc import ABC, abstractmethod


class Builder(ABC):
    @abstractmethod
    def set_name(self, name: str) -> "Builder":
        pass

    @abstractmethod
    def set_buy_price(self) -> "Builder":
        pass

    @abstractmethod
    def set_fail_price(self) -> "Builder":
        pass

    @abstractmethod
    def set_vaal_price(self) -> "Builder":
        pass

    @abstractmethod
    def set_success_price(self) -> "Builder":
        pass

    @abstractmethod
    def set_listed_successful(self) -> "Builder":
        pass

    @abstractmethod
    def set_leveled_price(self) -> "Builder":
        pass

    @abstractmethod
    def set_listed_leveled(self) -> "Builder":
        pass

    @abstractmethod
    def set_leveled_profit(self) -> "Builder":
        pass
