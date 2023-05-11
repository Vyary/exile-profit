class DivCard:
    def __init__(
        self,
        name: str = "",
        stack_size: int = 0,
        card_price: float = 0.0,
        reward_count: int = 0,
        reward: str = "",
        reward_price: float = 0.0,
        investment: float = 0.0,
        profit: float = 0.0,
    ):
        self.name = name
        self.stack_size = stack_size
        self.card_price = card_price
        self.reward_count = reward_count
        self.reward = reward
        self.reward_price = reward_price
        self.total_investment = investment
        self.profit = profit

    @classmethod
    def create_divination_card(
        cls,
        name: str,
        stack_size: int,
        card_price: float,
        reward_count: int,
        reward: str,
        reward_price: float,
        investment: float,
        profit: float,
    ) -> "DivCard":
        return DivCard(
            name,
            stack_size,
            card_price,
            reward_count,
            reward,
            reward_price,
            investment,
            profit,
        )
