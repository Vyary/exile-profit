from dataclasses import dataclass


@dataclass
class Gem:
    """
    Class for gem objects

    Parameters
        name : Gem's name
        base_price : Buy price of the gem
        fail_price : Price of unsuccessful corruption
        success_price : Price of successful corruption
        vaal_price : Price of vaal/semi-fail corruption
        listed : How many successful gems of set gem are listed on 
            the market including offline offerings
    """

    # Keep track of gems
    dictionary = {}

    name: str
    base_price: float = 0
    fail_price: float = 0
    success_price: float = 0
    vaal_price: float = 0
    listed: float = 0

    def __repr__(self):
        return self.name
