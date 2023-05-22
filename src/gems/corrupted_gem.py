from gems.gem import Gem


class CorruptedGem(Gem):
    def __init__(self):
        self.name: str = ""
        self.buy_price: float = 0
        self.fail_price: float = 0
        self.success_price: float = 0
        self.listed_successful: int = 0
        self.vaal_price: float = 0
        self.trade_link: str = ""

    def __str__(self) -> str:
        return (
            f"Gem info: \n"
            f"Name: {self.name}\n"
            f"Buy price: {self.buy_price}\n"
            f"Fail price: {self.fail_price}\n"
            f"Success price: {self.success_price}, \n"
            f"Number of listed successful gems: {self.listed_successful}\n"
            f"Vaal price: {self.vaal_price}\n"
        )
