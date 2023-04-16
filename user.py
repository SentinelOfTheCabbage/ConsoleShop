from basket import *

class User():

    def __init__(self, user_id, name, phase, order_id, basket = Basket()):
        self.id         = int(user_id)
        self.name       = name
        self.order_id   = int(order_id)
        self.basket     = basket
        self.phase      = int(phase)

    def add_to_basket(product):
        self.basket.add_to_basket(product)

    def __repr__(self):
        return f'User({self.id}, {self.name}, {self.phase}, {self.basket})'

    def __str__(self):
        return self.__repr__()