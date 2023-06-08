from items.item import Item


class BasicItem(Item):
    def __init__(self, name: str = "", drop_rate: float = 0, price: float = 0):
        self.name = name
        self.drop_rate = drop_rate
        self.price = price

    @classmethod
    def create_item(cls, name: str, drop_rate: float, price: float) -> "Item":
        return cls(name, drop_rate, price)
