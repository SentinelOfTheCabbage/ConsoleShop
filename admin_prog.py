from common import catalogue, DocEditor
from user import User
from admin_phases import admin_panel

def what_s_next():
    print('Что будем делать?\n')
    UPDATE_PRICE = '1'
    UPDATE_AMOUNT = '2'
    UPDATE_ORDER = '3'
    return_values = {
        UPDATE_PRICE: ('UPDATE_PRICE', 0), UPDATE_AMOUNT: ('UPDATE_AMOUNT', 2),
        UPDATE_ORDER : ('UPDATE_ORDER' , 4)
    }

    print(f'Введите {UPDATE_PRICE}, если хотите изменить стоимость продуктов')
    print(f'Введите {UPDATE_AMOUNT}, если хотите изменить количество товара на складе')
    # print(f'Введите {SHOW_ORDERS}, если хотите просмотреть заказы\n')
    print(f'Введите {UPDATE_ORDER}, если хотите изменить статус заказа')
    answer = input(': ')
    if answer in return_values:
        return return_values[answer]
    elif answer == '':
        return 'OUT', None
    else:
        print('Неверный ввод. Повторите попытку')
        return None, None

def main():
    return_values = ['UPDATE_PRICE', 'UPDATE_AMOUNT', 'SHOW_ORDERS', 'UPDATE_ORDER']
    OUT = 'OUT'

    documents = DocEditor()
    while True:
        wtd, phase = what_s_next()
        if wtd in return_values:
            break
        if wtd == OUT:
            return None

    argument = None
    while True:
        admin_panel[phase].on_call(argument, documents)
        answer = input(': ')

        if answer == '':
            break

        ans_status = admin_panel[phase].check_access(argument, answer, documents)

        if ans_status == True:
            argument = admin_panel[phase].on_return(argument, answer, documents)
        else:
            print('Неверный ввод! Повторите попытку')
            continue

        phase += 1

        if argument == 'END':
            break


if __name__ == '__main__':
    LOGGING   = '1'
    CATALOGUE = '2'
    EXIT_PROG = 'X'
    while True:
        print('На любом этапе нажмите ENTER для выхода в главное меню')
        print(f'Введите {LOGGING}, если хотите перейти в панель администратора')
        print(f'Введите {CATALOGUE}, если хотите просмотреть каталог')
        print(f'Введите {EXIT_PROG}, если вы хотите выйти из приложения')

        answer = input(': ')
        if answer == LOGGING:
            main()
        elif answer == CATALOGUE:
            catalogue()
        elif answer.upper() in ['X','Х']: # Rus + Eng X character
            break
        else:
            print('<-------------------------->')
            print('Неверный ввод')
