import random as ran
import sqlite3
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS card (id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)')
conn.commit()
id = 0
card_num = 0
pin_num = 0


def delete_acc():
    load_data = [card_num]
    cur.execute("DELETE FROM card WHERE number = ?;", load_data)
    conn.commit()
    print('The account has been closed!')


def check_acc(card_num):
    load_data = [card_num]
    cur.execute("SELECT * FROM card WHERE number=?;", load_data)
    output = cur.fetchone()
    if output:
        return True

    else:
        return False


def check_luhn(card_num):
    card_num_list = [int(x) for x in str(card_num)]
    middle_num_list = card_num_list[::2]
    sec_num_list = card_num_list[1::2]
    middle_num_list = [int(x) * 2 for x in middle_num_list]
    middle_num_list = [int(x) - 9 if int(x) > 9 else int(x) for x in middle_num_list]
    middle_num = (sum(middle_num_list) + sum(sec_num_list)) % 10
    if middle_num == 0:
        return True
    else:
        return False


def do_transfer(from_card, to_card, ammount):
    load_data = [ammount, from_card]
    cur.execute("UPDATE card SET balance = balance - ? WHERE number = ?;", load_data)
    load_data = [ammount, to_card]
    cur.execute("UPDATE card SET balance = balance + ? WHERE number = ?;", load_data)
    conn.commit()
    print('Success!')


def add_income(card_num, income):
    load_data = [income, card_num]
    cur.execute("UPDATE card SET balance = balance + ? WHERE number = ?;", load_data)
    conn.commit()
    print('Income was added!')


def check_balance(card_num):
    load_data = [card_num]
    cur.execute("SELECT * FROM card WHERE number=?;", load_data)
    balance = cur.fetchone()
    return balance[3]


def authorise(card_num, pin_num):
    load_data = [card_num, pin_num]
    cur.execute("SELECT * FROM card WHERE number=? AND pin=?;", load_data)
    output = cur.fetchone()

    if output:
        return True

    else:
        return False


def create_luhn(card_num):
    card_num_list = [int(x) for x in str(card_num)]
    middle_num_list = card_num_list[::2]
    sec_num_list = card_num_list[1::2]
    middle_num_list = [int(x) * 2 for x in middle_num_list]
    middle_num_list = [int(x) - 9 if int(x) > 9 else int(x) for x in middle_num_list]
    middle_num = 10 - ((sum(middle_num_list) + sum(sec_num_list)) % 10)

    if middle_num == 10:
        middle_num = 0
    card_num = str(card_num) + str(middle_num)
    return card_num


def create_account():
    card_num = ran.randint(111111111, 999999999)
    card_num = '400000' + str(card_num)
    card_num = create_luhn(card_num)
    return card_num


def create_pin():
    pin_num = ran.randint(1111, 9999)
    return pin_num


while True:
    print(f'1. Create an account\n2. Log into account\n0. Exit')
    choice = input()

    if choice == '1':
        card_num = create_account()
        pin_num = create_pin()
        print(f'Your card has been created\nYour card number:\n{card_num}\nYour card PIN:\n{pin_num}')
        load_data = [id, card_num, pin_num, '0']
        cur.execute("INSERT INTO card VALUES(?, ?, ?, ?);", load_data)
        authorise(card_num, pin_num)
        conn.commit()
    elif choice == '2':
        print('Enter your card number: ')
        card_num = int(input())
        print('Enter your PIN: ')
        pin_num = int(input())

        if authorise(card_num, pin_num):
            print('You have successfully logged in!')

            while True:
                print('1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit')
                choice = input()

                if choice == '1':
                    print(f'Balance: {check_balance(card_num)}')
                elif choice == '2':
                    print('Enter income: ')
                    income = int(input())
                    add_income(card_num, income)
                elif choice == '3':
                    print('Enter card number: ')
                    check_num = int(input())

                    if not check_luhn(check_num):
                        print('Probably you made a mistake in the card number. Please try again!')
                    elif not check_acc(check_num):
                        print('Such a card does not exist.')
                    else:
                        print('Enter how much money you want to transfer: ')
                        ammount = int(input())

                        if check_balance(card_num) > ammount:
                            do_transfer(card_num, check_num, ammount)
                        else:
                            print('Not enough money!')
                elif choice == '4':
                    delete_acc()
                    break
                elif choice == '5':
                    break
                elif choice == '0':
                    print('Bye!')
                    exit()
        else:
            print('Wrong card number or PIN!')
    elif choice == '0':
        break