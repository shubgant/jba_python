import random
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS card ('
            'id INTEGER,'
            'number TEXT,'
            'pin TEXT,'
            'balance INTEGER DEFAULT 0);')
conn.commit()
last_id = 0
login_pairs = {}


def unique_num_gen(length):
    return "".join([str(random.randint(0, 9)) for _ in range(0, length)])


def menu_printer(options):
    for idx, opt in enumerate(options):
        print(f"{idx + 1}. {opt}")
    print("0. Exit")
    return input()


def update_details():
    global last_id, login_pairs
    cur.execute('SELECT * from card;')
    id_list = cur.fetchall()
    login_pairs = {}
    if len(id_list) < 1:
        return
    last_id = id_list[-1][0]
    for c in id_list:
        login_pairs[c[1]] = [c[2], c[3]]


class Card:
    card_num = None
    pin = None
    balance = None

    def gen_new(self):
        acc_num = unique_num_gen(9)
        c_num_short = "400000" + acc_num
        checksum = self.luhn_algo(c_num_short)
        self.card_num = c_num_short + checksum
        self.pin = unique_num_gen(4)
        print("Your card number:", self.card_num, "Your card PIN:", self.pin, sep="\n")
        self.balance = 0
        cur.execute(f'INSERT INTO card (id, number, pin) VALUES ({last_id + 1}, {self.card_num}, {self.pin});')
        conn.commit()

    def detail_check(self):
        attempt_number = input("Enter your card number:\n")
        attempt_pin = input("Enter your PIN:\n")
        if login_pairs.get(attempt_number) and login_pairs.get(attempt_number)[0] == attempt_pin:
            print("You have successfully logged in!")
            self.card_num = attempt_number
            self.pin = attempt_pin
            self.balance = login_pairs[attempt_number][1]
            return True
        else:
            print("Wrong card number or PIN!")
            return False

    def add_income(self):
        amount = input("Enter income:\n")
        cur.execute(f'UPDATE card SET balance = balance + {amount} WHERE number = {self.card_num}')
        conn.commit()
        print("Income was added!")
        self.balance += int(amount)

    def transfer_income(self):
        target = input("Enter card number:\n")
        if target == self.card_num:
            print("You can't transfer money to the same account!")
        elif self.luhn_algo(target[:-1]) != target[-1]:
            print("Probably you made a mistake in the card number. Please try again!")
        elif not login_pairs.get(target):
            print("Such a card does not exist.")
        else:
            amount = input("Enter how much money you want to transfer:\n")
            if int(amount) > int(self.balance):
                print("Not enough money!")
            else:
                cur.execute(f'UPDATE card SET balance = balance - {amount} WHERE number = {self.card_num}')
                cur.execute(f'UPDATE card SET balance = balance + {amount} WHERE number = {target}')
                conn.commit()
                self.balance -= int(amount)
                print("Success!")

    def delete_account(self):
        cur.execute(f'DELETE FROM card WHERE number = {self.card_num}')
        conn.commit()
        print("The account has been closed!")

    @staticmethod
    def luhn_algo(card_number):
        l_nums = [int(n) for n in list(card_number)]
        step1 = [n * 2 if idx % 2 == 0 else n for idx, n in enumerate(l_nums)]
        step2 = [n - 9 if n > 9 else n for n in step1]
        return str((10 - (sum(step2))) % 10)


card = Card()
logged_in = 0
while True:
    update_details()
    if not logged_in:
        usr_choice = menu_printer(["Create an account", "Log into account"])
        if usr_choice == "0":
            print("Bye!")
            break
        elif usr_choice == "1":
            card.gen_new()
        elif usr_choice == "2":
            if not login_pairs:
                print("No cards in system!")
            elif card.detail_check():
                logged_in = 1
    elif logged_in:
        logged_in_choice = menu_printer(["Balance", "Add income", "Do transfer", "Close account", "Log out"])
        if logged_in_choice == "0":
            print("Bye!")
            break
        elif logged_in_choice == "1":
            print("Balance:", card.balance)
        elif logged_in_choice == "2":
            card.add_income()
        elif logged_in_choice == "3":
            card.transfer_income()
        elif logged_in_choice == "4":
            card.delete_account()
            logged_in = 0
        elif logged_in_choice == "5":
            print("You have successfully logged out!")
            logged_in = 0
