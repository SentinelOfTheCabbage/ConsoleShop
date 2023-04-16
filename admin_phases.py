from common import Phase

# ------------------------------------------------------------------
# ------------------------- Admin phase 1 --------------------------
# --------------------------CHANGE PRICE----------------------------
phase_1 = Phase()


def p1_on_call(argument, documents):
    print('На текущий момент в магазине имется:')

    products = documents.get_products()
    for pos, elem in enumerate(products):
        print(f'{pos + 1} {elem}')

    print('Введите соответствующую цифру товара для изменения цены.')


def p1_check_access(argument, message, documents):
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


def p1_on_return(argument, message, documents):
    return int(message)

setattr(phase_1, 'on_call', p1_on_call)
setattr(phase_1, 'check_access', p1_check_access)
setattr(phase_1, 'on_return', p1_on_return)


# ------------------------------------------------------------------
# ------------------------- Admin phase 2 --------------------------
# ----------------------------NEW VALUE-----------------------------
phase_2 = Phase()


def p2_on_call(argument, documents):

    product = documents.get_products()[argument - 1]
    print(f'Вы выбрали {product.name}.')
    print(f'Текущая цена одной единицы - {product.price} рублей')
    print('Введите новое значение')


def p2_check_access(argument, message, documents):
    if message.isdigit() and int(message) > 0:
        return True
    else:
        return False


def p2_on_return(argument, message, documents):
    documents.update_product_price(argument, int(message))
    print('Обновлено')
    return 'END'

setattr(phase_2, 'on_call', p2_on_call)
setattr(phase_2, 'check_access', p2_check_access)
setattr(phase_2, 'on_return', p2_on_return)


# ------------------------------------------------------------------
# ------------------------- Admin phase 3 --------------------------
# --------------------------CHANGE AMOUNT---------------------------
phase_3 = Phase()


def p3_on_call(arument, documents):
    print('На текущий момент в магазине имется:')

    products = documents.get_products()
    for pos, elem in enumerate(products):
        print(f'{pos + 1} {elem}')

    print('Введите соответствующую цифру товара для изменения количества на складе.')


def p3_check_access(argument, message, documents):
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


def p3_on_return(argument, message, documents):
    return int(message)

setattr(phase_3, 'on_call', p3_on_call)
setattr(phase_3, 'check_access', p3_check_access)
setattr(phase_3, 'on_return', p3_on_return)


# ------------------------------------------------------------------
# ------------------------- Admin phase 4 --------------------------
# --------------------------- NEW VALUE ----------------------------
phase_4 = Phase()


def p4_on_call(argument, documents):
    product = documents.get_products()[argument - 1]
    print(f'Вы выбрали {product.name}.')
    print(f'Текущие объемы товара - {product.amount} штук')
    print('Введите новое значение')



def p4_check_access(argument, message, documents):
    if message.isdigit() and int(message) > 0:
        return True
    else:
        return False

def p4_on_return(argument, message, documents):
    documents.update_product_amount(argument, int(message))
    print('Обновлено')
    return 'END'

setattr(phase_4, 'on_call', p4_on_call)
setattr(phase_4, 'check_access', p4_check_access)
setattr(phase_4, 'on_return', p4_on_return)


# ------------------------------------------------------------------
# ------------------------- Admin phase 5 --------------------------
# ---------------------------ORDERS LIST----------------------------
phase_5 = Phase()


def p5_on_call(argument, documents):
    print('На текущий момент следующие заказы не доставлены:')

    products = documents.get_orders()
    for pos, elem in enumerate(products):
        print(f'{pos + 1} {elem}')

    print('Введите соответствующую цифру заказа для изменения его статуса.')


def p5_check_access(argument, message, documents):
    possible_answers = list(
        map(
            str,
            range(
                1,
                len(documents.get_orders()) + 1)
        )
    )
    if message in possible_answers:
        return True
    else:
        return False


def p5_on_return(argument, message, documents):
    return int(message)

setattr(phase_5, 'on_call',         p5_on_call)
setattr(phase_5, 'check_access',    p5_check_access)
setattr(phase_5, 'on_return',       p5_on_return)


# ------------------------------------------------------------------
# ------------------------- Admin phase 6 --------------------------
# --------------------------UPDATE STATUS---------------------------
phase_6 = Phase()


def p6_on_call(argument, documents):
    print('Какой статус для этого заказа вы хотите установить?\n')

    print('Введите 1, если хотите установить значение статуса "Отправлен"')
    print('Введите 2, если хотите установить значение статуса "Доставлен"')

    print('Введите соответствующую цифру для изменения статуса заказа.')

def p6_check_access(argument, message, documents):
    if message in ['1','2']:
        return True
    else:
        return False


def p6_on_return(argument, message, documents):
    documents.update_order_status(argument, int(message))
    return 'END'

setattr(phase_6, 'on_call',         p6_on_call)
setattr(phase_6, 'check_access',    p6_check_access)
setattr(phase_6, 'on_return',       p6_on_return)

admin_panel = [phase_1, phase_2, phase_3, phase_4, phase_5, phase_6]
