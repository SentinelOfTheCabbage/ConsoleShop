from product import *
from copy import deepcopy

class Basket():

    def __init__(self, backpack=[]):
        self.backpack = backpack

    def __len__(self):
        return len(self.backpack)

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        if self.i == len(self.backpack) or len(self.backpack) == 0:
            raise StopIteration
        else:
            self.i += 1
            return self.backpack[self.i - 1]

    def add_to_basket(self, product):

        for pos, elem in enumerate(self.backpack):
            if self.__same_products(elem, product):
                self.backpack[pos] = self.__union_products(elem, product)
                self.backpack = self.backpack[:pos] + self.backpack[pos + 1:] + [self.backpack[pos]]
                return None

        self.backpack.append(product)

    def __same_products(self, first, second):
        if first.name == second.name:
            return True
        else:
            return False

    def __union_products(self, first, second):
        first.amount += second.amount
        return first

    def get_by_name(self, product_name):
        for product in self.backpack:
            if product.name == product_name:
                return product
        else:
            return None

    def update_product(self, product):
        for pos, elem in enumerate(self.backpack):
            if elem.name == product.name:
                self.backpack[pos] = product
                return True
        else:
            return False

    def update_by_index(self, index, amount):
        product = deepcopy(self.backpack[index])
        product.amount = amount
        self.add_to_basket(product)

    def get_last(self):
        return self.backpack[-1]

    def remove(self, index):
        self.backpack = self.backpack[:index] + self.backpack[index + 1:]

    def __repr__(self):
        return f'Basket({self.backpack})'

    def get_as_list(self, prices):
        res = []
        for pos, prod in enumerate(self.backpack):
            unit_price = prices[prod.name]
            self.backpack[pos].price = unit_price * prod.amount
            line = f'- {prod.name} x {prod.amount} = {prod.amount*unit_price} руб.'
            res.append(line)
        return res

    def get_sum(self):
        s = 0
        for product in self.backpack:
            s += product.price
        return s

    def not_empty(self):
        return len(self.backpack) > 0