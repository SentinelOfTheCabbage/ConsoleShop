from pandas import read_csv
from user import User
from basket import Basket
from datetime import datetime

class DocEditor():

    def __init__(self):
        self.__basket = 'orders_content.csv'# Список товаров из заказов
        self.__users_list = 'users_list.csv'# Список пользователей
        self.__orders = 'orders.csv'        # Список заказов
        self.__products = 'products.csv'    # Список продуктов
        self.__order_id = 'last_order_id'   # тут хранится очередной номер для заказа.

    def get_products(self):
        products = []
        file_content = read_csv(self.__products, sep=';')
        file_content = file_content[file_content.amount > 0]

        for elem in file_content.itertuples():
            product = SkladProduct(elem.name, elem.amount, elem.price)
            products.append(product)
        return products

    def find_user(self, login, password):
        users_list = read_csv(self.__users_list, sep=';')
        user_line = users_list[(users_list.login == login) & (users_list.password == password)]
        if len(user_line) == 0:
            return None

        user_id = int(user_line.user_id)
        user = self.__check_last_visit(user_id)
        if user != None:
            user = self.__check_basket(user)
            return user
        else:
            u = user_line
            return User(int(u.user_id), str(u.name), 0, self.__get_oid())

    def __check_last_visit(self, user_id):
        orders_list = read_csv(self.__orders, sep=';')
        CREATED_STATS = list('01234')

        line = orders_list[
            (orders_list.user_id == user_id) &
            (orders_list.status.isin(CREATED_STATS))
            ]

        if len(line) == 0 :
            return None
        elif len(line) == 1:
            orders_list = orders_list.drop(line.index)
            result = self.get_user(int(line.order_id), int(line.status))
            orders_list.to_csv(self.__orders, sep=';', index=False)
            return result
        else:
            raise Exception('В таблице слишком много созданных и незавершенных заказов для одного пользователя =/')

    def __get_oid(self):
        with open(self.__order_id, 'r', encoding='utf-8') as source:
            order_id = int(source.read())

        with open(self.__order_id, 'w', encoding='utf-8') as gate:
            gate.write(str(order_id + 1))

        return order_id

    def get_user(self, order_id, phase):
        orders = read_csv(self.__orders, sep=';')
        k = orders[orders.order_id == order_id]
        if len(k) == 1:
            user_id = int(k.user_id)

            users = read_csv(self.__users_list, sep=';')
            user = users[users.user_id == user_id]

            products = read_csv(self.__basket, sep=';')

            b = products[products.order_id == order_id]
            products = products.drop(b.index)
            products.to_csv(self.__basket, sep=';', index=False)
            basket = Basket([])

            for p in b.itertuples():
                product = UserProduct(p.product_name, p.amount)
                basket.add_to_basket(product)

            return User(int(user.user_id[0]), str(user.name[0]), phase, self.__get_oid(), basket)

        else:
            raise Exception('Как я сюда попал?')

    def get_amount(self, product):
        products = read_csv(self.__products, sep=';')
        amount = int(products[products.name == product.name].amount) - product.amount
        return amount

    def get_prices(self):
        products = read_csv(self.__products, sep=';')
        products = products[['name', 'price']]
        res = {}
        for p in products.itertuples():
            res[p.name] = p.price
        return res

    def end_order(self, user, status):
        orders = read_csv(self.__orders, sep=';')
        new_order = {}
        new_order['order_id'] = user.order_id
        new_order['user_id'] = user.id
        new_order['datetime'] = datetime.now().isoformat()
        if status == 'END':
            new_order['status'] = 'PAYED'
            self.update_products(user.basket)
        else:
            phases_shift = {
                0:0, 1:1, 2:2,
                3:2, 4:2
            }
            new_order['status'] = phases_shift[user.phase]

        orders = orders.append(new_order, ignore_index=True)
        orders.to_csv(self.__orders, sep=';', index=False)

        orders_content = read_csv(self.__basket, sep=';')

        orders_content = orders_content.drop(
            orders_content[
                orders_content.order_id == user.order_id
            ].index
        )

        for product in user.basket:
            line = {}
            line['order_id'] = user.order_id
            line['product_name'] = product.name
            line['amount'] = product.amount
            line['price'] = product.price
            orders_content = orders_content.append(line, ignore_index=True)

        orders_content.to_csv(self.__basket, sep=';', index=False)

    def display_orders(self, user):
        orders = read_csv(self.__orders, sep=';')
        orders = orders[orders.user_id == user.id]
        orders_content = read_csv(self.__basket, sep=';')
        statuses = {
            '01234'     : 'Не завершён',
            'PAYED'     : 'Оплачен',
            'SENT'      : 'Отправлен',
            'DELIVERED' : 'Доставлен'
        }

        for o in orders.itertuples():
            if o.status in '01234':
                status = 'Не завершён'
            else:
                status = statuses[o.status]
            print(f'- Заказ №{o.order_id}. Статус : {status}')

            products = orders_content[orders_content.order_id == o.order_id]
            for p in products.itertuples():
                if p.price > 0:
                    print(f'\t + {p.product_name} х {p.amount} = {p.price} руб')
                else:
                    print(f'\t + {p.product_name} х {p.amount}')

        if user.basket.not_empty():
            print(f'- Заказ №{user.order_id}. Статус : Не завершён')
            for p in user.basket:
                print(f'\t + {p.name} x {p.amount}')

    def update_products(self, basket):
        products = read_csv(self.__products, sep=';')

        for product in basket:
            products.loc[products.name == product.name, 'amount'] -= product.amount

        products.to_csv(self.__products, sep=';', index=False)

    def __check_basket(self,user):
        products = read_csv(self.__products, sep=';')

        for pos, unit in enumerate(user.basket):
            if (products.loc[(products.name == unit.name), 'amount'] < unit.amount).values[0]:
                print(f'~ Продукт {unit.name} был удалён из корзины, из-за недостаточности его на складе')
                user.basket.remove(pos)

        return user

    def update_product_price(self, product_id, new_price):
        products = read_csv(self.__products, sep=';')
        products.loc[product_id - 1, 'price'] = new_price
        products.to_csv(self.__products, sep=';', index=False)

    def update_product_amount(self, product_id, new_amount):
        products = read_csv(self.__products, sep=';')
        products.loc[product_id - 1, 'amount'] = new_amount
        products.to_csv(self.__products, sep=';', index=False)

    def get_orders(self):
        orders = read_csv(self.__orders, sep=';')
        statuses = {
            'PAYED'     : 'Оплачен',
            'SENT'      : 'Отправлен',
        }
        orders = orders[orders.status.isin(statuses)]
        orders_content = read_csv(self.__basket, sep=';')
        orders_list = []
        for o in orders.itertuples():
            status = statuses[o.status]
            orders_list.append(f'- Заказ №{o.order_id}. Статус: {status}')
            products = orders_content[orders_content.order_id == o.order_id]

            for p in products.itertuples():
                orders_list[-1] += f'\n\t + {p.product_name} x {p.amount} = {p.price} руб'
        return orders_list

    def update_order_status(self, argument, message):
        orders = read_csv(self.__orders, sep=';')
        statuses_1 = {
            'PAYED'     : 'Оплачен',
            'SENT'      : 'Отправлен',
        }
        statuses_2 = {
            1: 'SENT',
            2: 'DELIVERED'
        }
        needed_order_id = orders[orders.status.isin(statuses_1)].iloc[argument - 1].order_id
        orders.loc[(orders.status.isin(statuses_1)) & (orders.order_id == needed_order_id), 'status'] = statuses_2[message]
        orders.to_csv(self.__orders, sep=';', index=False)

def catalogue():
    products = DocEditor().get_products()
    print('В текущий момент мы готовы предоставить вам:')
    for product in products:
        print(product)


class Phase():

    def on_call(user, documents):
        pass

    def on_return(user, message, documents):
        pass

    def check_access(user, message, documents):
        pass

class UserProduct():

    def __init__(self, name, amount):
        self.name = name
        self.amount = int(amount)
        self.price = 0

    def __str__(self):
        return f'- {self.name} x {self.amount}'

    def __repr__(self):
        return f'UserProduct({self.name}, {self.amount})'

class SkladProduct():

    def __init__(self, name, amount, price):
        self.name = name
        self.amount = amount
        self.price = price

    def __str__(self):
        return f'- {self.name} (на складе {self.amount} шт.) по {self.price} руб/шт.'