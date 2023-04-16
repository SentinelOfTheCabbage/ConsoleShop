from common import catalogue, DocEditor
from user import User
from user_phases import shop

def login():
    print('Введите ваш логин')
    login = input(': ')

    print('Введите ваш пароль')
    password = input(': ')

    user = DocEditor().find_user(login, password)
    if user == None:
        print('Некорректные данные. Повторите ввод')
        return None
    return user

def what_s_next():
    print('Что вы хотите сделать далее?\n')
    SHOW_ORDERS = '1'
    CREATE_ORDER = '2'
    return_values = {SHOW_ORDERS:'SHOW_ORDERS', CREATE_ORDER:'CREATE_ORDER'}

    print(f'Введите {SHOW_ORDERS}, если хотите просмотреть список своих заказов')
    print(f'Введите {CREATE_ORDER}, если хотите создать или продолжить заказ\n')
    answer = input(': ')
    if answer in [SHOW_ORDERS, CREATE_ORDER]:
        return return_values[answer]
    elif answer == '':
        return 'OUT'
    else:
        print('Неверный ввод. Повторите попытку')
        return None

def main():
    user = None
    CREATE_ORDER = 'CREATE_ORDER'
    SHOW_ORDERS = 'SHOW_ORDERS'
    OUT = 'OUT'

    documents = DocEditor()
    while True:
        user = login()
        if user != None:
            break

    while True:
        wtd = what_s_next()
        if wtd in [SHOW_ORDERS, CREATE_ORDER]:
            break
        if wtd == OUT:
            documents.end_order(user, None)
            return None

    if wtd == CREATE_ORDER:
        while True:

            shop[user.phase].on_call(user, documents)
            answer = input(': ')

            if answer == '':
                documents.end_order(user, None)
                break

            ans_status = shop[user.phase].check_access(user, answer, documents)

            if ans_status == True:
                user, argument = shop[user.phase].on_return(user, answer, documents)
            else:
                print('Неверный ввод! Повторите попытку')
                continue

            if argument == 'END':
                documents.end_order(user, argument)
                break
    elif wtd == SHOW_ORDERS:
        documents.display_orders(user)
        documents.end_order(user, None)


if __name__ == '__main__':
    LOGGING   = '1'
    CATALOGUE = '2'
    EXIT_PROG = 'X'
    while True:
        print('На любом этапе нажмите ENTER для выхода в главное меню')
        print(f'Введите {LOGGING}, если хотите войти')
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
