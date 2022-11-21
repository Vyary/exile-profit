class Gem:
    gem_lst = []

    def __init__(self, name, base_price=0, fail_price=0, success_price=0, vaal_price=0, listed=0):
        """
        Class holding gem objects attributes
        :param name: Gem's name
        :param base_price: Buy price of the gem
        :param fail_price: Price of unsuccessful corruption
        :param success_price: Price of successful corruption
        :param vaal_price: Price of vaal/semi-fail corruption
        :param listed: How many successful set gem are listed on the market including offline listings
        """
        self.name = name
        self.base_price = base_price
        self.fail_price = fail_price
        self.success_price = success_price
        self.vaal_price = vaal_price
        self.listed = listed

    def __repr__(self):
        return self.name
