from dataclasses import dataclass


@dataclass
class Gem:
    # Keep track of gems
    gem_lst = []
    """
    Class for gem objects
    :param name: Gem's name
    :param base_price: Buy price of the gem
    :param fail_price: Price of unsuccessful corruption
    :param success_price: Price of successful corruption
    :param vaal_price: Price of vaal/semi-fail corruption
    :param listed: How many successful gems of set gem are listed
        on the market including offline offerings
    """
    name: str
    base_price: float = 0
    fail_price: float = 0
    success_price: float = 0
    vaal_price: float = 0
    listed: float = 0

    def __repr__(self):
        return self.name
