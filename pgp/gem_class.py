class Gem:
    gem_lst = []

    def __init__(self, name, base_price=0, fail_price=0, success_price=0, vaal_price=0, listed=0):
        self.name = name
        self.base_price = base_price
        self.fail_price = fail_price
        self.success_price = success_price
        self.vaal_price = vaal_price
        self.listed = listed

    def __repr__(self):
        return self.name
