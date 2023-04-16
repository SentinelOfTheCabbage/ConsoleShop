from common import Phase

# ------------------------------------------------------------------
# -------------------------- Shop phase 1 --------------------------
# --------------------------SELECT PRODUCT--------------------------
phase_1 = Phase()


def p1_on_call(user, documents):
    print('На текущий момент в магазине имется:')

    products = documents.get_products()
    for pos, elem in enumerate(products):
        for p in user.basket:
            if p.name == elem.name:
                elem.amount -= p.amount
        print(f'{pos + 1} {elem}')

    print('Введите соответствующую цифру товара для приобретения.')


def p1_check_access(user, message, documents):
    possible_answers = list(
        map(
            str,
            range(
                1,
                len(documents.get_products()) + 1)
        )
    )

    if message in possible_answers:
        return True
    else:
        return False


def p1_on_return(user, message, documents):
    product = documents.get_products()[int(message) - 1]
    product.amount = 0
    user.basket.add_to_basket(product)
    user.phase += 1
    return user, None

setattr(phase_1, 'on_call', p1_on_call)
setattr(phase_1, 'check_access', p1_check_access)
setattr(phase_1, 'on_return', p1_on_return)


# ------------------------------------------------------------------
# -------------------------- Shop phase 2 --------------------------
# --------------------------SELECT AMOUNT---------------------------
phase_2 = Phase()


def p2_on_call(user, documents):
    amount = documents.get_amount(user.basket.get_last())
    print(f'Введите необходимый объем в штуках (доступно {amount} шт.)')


def p2_check_access(user, message, documents):
    amount = documents.get_amount(user.basket.get_last())
    possible_answers = list(
        map(
            str,
            range(0, amount + 1)
        )
    )

    if message in possible_answers:
        return True
    else:
        return False


def p2_on_return(user, message, documents):
    user.basket.update_by_index(-1, int(message))

    user.phase += 1
    return user, None

setattr(phase_2, 'on_call', p2_on_call)
setattr(phase_2, 'check_access', p2_check_access)
setattr(phase_2, 'on_return', p2_on_return)


# ------------------------------------------------------------------
# -------------------------- Shop phase 3 --------------------------
# -------------------------SELECT NEXT WAY--------------------------
phase_3 = Phase()


def p3_on_call(user, documents):
    print('Ваша корзина:')

    prices = documents.get_prices()
    products = user.basket.get_as_list(prices)

    print('\n'.join(products))

    print('\nЧто вы хотите сделать далее?')
    print('Введите 1, если хотите добавить продукт')
    print('Введите 2, если хотите удалить продукт')
    print('Введите 3, если хотите оформить заказ')


def p3_check_access(user, message, documents):
    if message in ['1', '2', '3']:
        if message == '3' and len(user.basket) == 0:
            print('Ваша корзина пуста!')
            return False
        return True
    else:
        return False


def p3_on_return(user, message, documents):
    if message == '1':
        user.phase -= 2
    elif message == '2':
        user.phase += 1
    elif message == '3':
        user.phase += 2
    return user, None

setattr(phase_3, 'on_call', p3_on_call)
setattr(phase_3, 'check_access', p3_check_access)
setattr(phase_3, 'on_return', p3_on_return)


# ------------------------------------------------------------------
# -------------------------- Shop phase 4 --------------------------
# ------------------------ Product remover -------------------------
phase_4 = Phase()


def p4_on_call(user, documents):
    print('Какой из продуктов вы хотите удалить?')
    for pos, product in enumerate(user.basket):
        print(f'{pos + 1})  {product}')

    print('Введите соответствующую цифру для удаления')


def p4_check_access(user, message, documents):
    possible_answers = list(
        map(str,
            range(1, len(user.basket) + 1)
            )
    )

    if message in possible_answers:
        return True
    else:
        return False


def p4_on_return(user, message, documents):
    index = int(message) - 1
    user.basket.remove(index)
    user.phase -= 1
    return user, None

setattr(phase_4, 'on_call', p4_on_call)
setattr(phase_4, 'check_access', p4_check_access)
setattr(phase_4, 'on_return', p4_on_return)


# ------------------------------------------------------------------
# -------------------------- Shop phase 5 --------------------------
# ----------------------------Order pay-----------------------------
phase_5 = Phase()


def p5_on_call(user, documents):
    sum_price = user.basket.get_sum()
    print(f'Общая стоимость заказа составляет {sum_price} рублей.')
    print(f'Для подтверждения оплаты заказа введите Y')


def p5_check_access(user, message, documents):
    if message in ['Y','y']:
        return True
    else:
        return False


def p5_on_return(user, message, documents):
    return user, 'END'

setattr(phase_5, 'on_call',         p5_on_call)
setattr(phase_5, 'check_access',    p5_check_access)
setattr(phase_5, 'on_return',       p5_on_return)

shop = [phase_1, phase_2, phase_3, phase_4, phase_5]
