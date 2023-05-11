from typing import Any, Dict, List

from divination_cards.div_card import DivCard
from divination_cards.div_card_creator import DivCardCreator
from utils.price_check.api_call import APICall
from utils.storage import Storage


class CombinedDivCardCreator(DivCardCreator):
    def __init__(
        self,
        divination_card_data: Dict[str, Dict[str, str]],
        massive_data: Dict[str, Dict[str, str]],
        divination_cards_queries: Dict[str, Any],
        price_check_method: APICall,
        divination_card_class: DivCard,
        storage: Storage,
    ):
        self.divination_card_data = divination_card_data
        self.massive_data = massive_data
        self.divination_cards_queries = divination_cards_queries
        self.price_check_method = price_check_method
        self.divination_card_class = divination_card_class
        self.storage = storage

    def __get_reward_price_from_massive_data(self, reward_name: str):
        if reward_name not in self.massive_data:
            return 0

        reward_price = self.massive_data[reward_name]["chaos"]
        return reward_price

    def __get_reward_price_average(self, div_card_name: str):
        rewards_prices: List[float] = []

        for current_reward in self.divination_cards_queries[div_card_name]:
            if current_reward in self.massive_data:
                current_reward_price = self.massive_data[current_reward]["chaos"]
                rewards_prices.append(float(current_reward_price))
            else:
                current_reward_price = self.price_check_method.get_price(
                    self.divination_cards_queries[div_card_name][current_reward]
                )
                rewards_prices.append(current_reward_price)

        rewards_average = float(sum(rewards_prices) / len(rewards_prices))
        return rewards_average

    def create_div_card(self):
        for div_card in self.divination_card_data:
            name = self.divination_card_data[div_card]["name"]
            stack_size = int(self.divination_card_data[div_card]["stack_size"])
            card_price = float(self.divination_card_data[div_card]["card_price"])
            reward_count = int(self.divination_card_data[div_card]["reward_count"])
            reward = self.divination_card_data[div_card]["reward"]
            reward_price = float(self.__get_reward_price_from_massive_data(reward))

            if reward_price == 0 and name in self.divination_cards_queries:
                reward_price = self.__get_reward_price_average(name)

            investment = float(f"{stack_size * card_price:.2f}")
            profit = float(f"{reward_price - investment:.2f}")

            current_div_card = self.divination_card_class.create_divination_card(
                name,
                stack_size,
                card_price,
                reward_count,
                reward,
                reward_price,
                investment,
                profit,
            )
            self.storage.add_item(current_div_card)
        return self.storage.inventory
