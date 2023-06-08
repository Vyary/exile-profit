from items.item import Item


class DivCard(Item):
    def __init__(
        self,
        name: str = "",
        wiki_link: str = "",
        stack_size: int = 0,
        card_price: float = 0.0,
        reward: str = "",
        reward_price: float = 0.0,
        investment: float = 0.0,
        profit: float = 0.0,
        trade_link: str = "",
    ):
        self.name = name
        self.wiki_link = wiki_link
        self.stack_size = stack_size
        self.card_price = card_price
        self.reward = reward
        self.reward_price = reward_price
        self.total_investment = investment
        self.profit = profit
        self.trade_link = trade_link

    @classmethod
    def create_divination_card(
        cls,
        name: str,
        wiki_link: str,
        stack_size: int,
        card_price: float,
        reward: str,
        reward_price: float,
        investment: float,
        profit: float,
        trade_link: str,
    ) -> "DivCard":
        return DivCard(
            name,
            wiki_link,
            stack_size,
            card_price,
            reward,
            reward_price,
            investment,
            profit,
            trade_link,
        )
