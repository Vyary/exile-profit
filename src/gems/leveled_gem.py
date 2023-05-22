from gems.gem import Gem


class LeveledGem(Gem):
    def __init__(self):
        self.name: str = ""
        self.buy_price: float = 0
        self.leveled_price: float = 0
        self.listed_leveled: int = 0
        self.profit: float = 0
        self.trade_link: str = ""

    def __str__(self) -> str:
        return (
            f"Gem info: \n"
            f"Name: {self.name}\n"
            f"Buy price: {self.buy_price}\n"
            f"Leveled Price: {self.leveled_price}\n"
            f"Number of listed leveled gems: {self.listed_leveled}\n"
            f"Profit: {self.profit}\n"
        )
