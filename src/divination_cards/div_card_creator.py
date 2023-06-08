from typing import Any, Dict, List

from tqdm import tqdm

from items.divination_card import DivCard
from poe_trade.poe_trade import PoeTrade
from storages.item_storage import ItemStorage


class DivCardCreator:
    def __init__(
        self,
        current_league: str,
        massive_data: Dict[str, Dict[str, str]],
        price_checker: PoeTrade,
        div_item_class: DivCard,
        items_cache: Dict[str, Any],
        storage: ItemStorage,
    ):
        self.current_league = current_league
        self.massive_data = massive_data
        self.price_checker = price_checker
        self.div_item_class = div_item_class
        self.items_cache = items_cache
        self.storage = storage

    def __get_item_price(self, item: str, query: Dict[str, Any]) -> float:
        if item in self.massive_data:
            return float(self.massive_data[item]["chaos"])

        if item in self.items_cache:
            return self.items_cache[item]

        item_price = self.price_checker.get_item_price(query)[0]

        if item not in self.items_cache:
            self.items_cache[item] = item_price

        return float(item_price)

    def __get_reward_price(self, reward: str, queries_values: Dict[str, Any]):
        prices: List[float] = []
        amount = 1

        for component, query in queries_values["components"].items():
            component = component.split(" | ")[0]

            if "x " in reward and reward[0].isdigit():
                amount, split_component = reward.split("x ")
                amount = int(amount)

                if component == reward:
                    component = split_component

            prices.append(self.__get_item_price(component, query))

        average_price = sum(prices) / len(prices)
        return amount * average_price

    def __create_trade_link(self, card_name: str) -> str:
        name_for_link = card_name.replace(" ", "%20")
        query = f"{{%22query%22:{{%22filters%22:{{%22type_filters%22:{{%22filters%22:{{%22category%22:{{%22option%22:%22card%22}}}}}}}},%22type%22:%22{name_for_link}%22}}}}"
        trade_link = f'=HYPERLINK("https://www.pathofexile.com/trade/search/{self.current_league}?q={query}","Trade")'
        return trade_link

    def div_cards_info(self, divination_cards_queries: Dict[str, Any]):
        div_cards_storage = self.storage.new_storage()

        for card, values in tqdm(
            divination_cards_queries.items(), desc="Divination Cards"
        ):
            wiki_link = f'=HYPERLINK("https://poewiki.net/wiki/{card}","Wiki")'
            stack_size = values["stack_size"]
            card_price = self.__get_item_price(card, values["div_card_query"])
            reward = values["reward"]
            reward_price = self.__get_reward_price(reward, values)
            investment = stack_size * card_price
            profit = reward_price - investment
            trade_link = self.__create_trade_link(card)

            current_div_card = self.div_item_class.create_divination_card(
                card,
                wiki_link,
                stack_size,
                card_price,
                reward,
                reward_price,
                investment,
                profit,
                trade_link,
            )
            div_cards_storage.add_item(current_div_card)

        return div_cards_storage.inventory
