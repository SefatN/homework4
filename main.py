from termcolor import colored


class InsufficientFundsError(Exception):
    pass


def display_items(items):
    print("Here are the available items:- ")
    for item, price in items.items():
        print(f"{item}: £{price}")


def get_user_choice(items):
    while True:
        choice = input("What would you like to buy?:- ")
        if choice == "exit":
            print("Goodbye!")
            exit()
        elif choice not in items:
            print("Invalid choice! Please choose again.")
        else:
            return choice


def get_additional_money():
    while True:
        additional_money = input("You do not have enough money. Do you have more? If so, how much? Type 0 to exit. ")
        if additional_money == '0':
            print("Goodbye!")
            exit()
        try:
            additional_money = int(additional_money)
            return additional_money
        except ValueError:
            print("Invalid input! Please enter a valid amount.")


def buy_item(choice, customer_money, items):
    if customer_money >= items[choice]:
        print(f"Here's your {choice}!")
        customer_money -= items[choice]
        return customer_money, 0
    else:
        attempts = 0
        additional_money = 0  # Initialize additional_money variable
        while attempts < 3:
            more_money = get_additional_money()
            additional_money += more_money  # Accumulate additional money entered by user
            customer_money += more_money  # Add additional money to customer's total money
            if customer_money >= items[choice]:
                print(f"Here's your {choice}!")
                customer_money -= items[choice]
                return customer_money, additional_money
            else:
                attempts += 1
        else:
            raise InsufficientFundsError("You do not have enough money for this item. Goodbye!")



def shop():
    items = {"bread": 50, "chips": 80, "milk": 120}
    customer_money = 100

    print(colored('Welcome to our shop!', 'cyan'))
    while True:
        display_items(items)
        try:
            choice = get_user_choice(items)
            customer_money, additional_money = buy_item(choice, customer_money, items)
        except ValueError as ve:
            print(ve)
        except InsufficientFundsError as ife:
            print(ife)
            break
        else:
            print(f"You have £{customer_money} left.")


if __name__ == '__main__':
    shop()
