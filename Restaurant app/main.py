import time
import sys
import getpass
import os
import sqlite3

clear = lambda: os.system('cls')
conn = sqlite3.connect('order_database.db')
c = conn.cursor()

def create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS orders (
                 username TEXT,
                 item TEXT,
                 price REAL
                 )''')
    conn.commit()

def insert_order(username, item, price):
    c.execute("INSERT INTO orders (username, item, price) VALUES (?, ?, ?)", (username, item, price))
    conn.commit()

def get_order_history(username):
    c.execute("SELECT item, price FROM orders WHERE username=?", (username,))
    orders = c.fetchall()
    total_bill = sum([order[1] for order in orders])
    return orders, total_bill

def close_connection():
    conn.close()

user_credentials = {}

def insert_user(username, password):
    global user_credentials
    user_credentials[username] = password

def username_exists(username):
    global user_credentials
    return username in user_credentials

def get_password(username):
    global user_credentials
    return user_credentials.get(username)

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def welcome_message():
    clear_console()
    print("Welcome to EatEase Pinoy Restaurant! Prepare to embark on a culinary journey of epic proportions!")
    time.sleep(1)
    print("")
    print("What would you like to do?")
    print("1: Login")
    print("2: Signup")
    print("3: Exit")
    choice = input("Enter your choice (1, 2, or 3): ")
    if choice == '1':
        login()
    elif choice == '2':
        signup()
    elif choice == '3':
        close_connection()
        print("Thank you for visiting EatEase Pinoy Restaurant! Goodbye!")
        sys.exit(0)
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")
        welcome_message()

def login():
    clear_console()
    global username
    username = input("Enter your username: ")
    if username_exists(username):
        password = getpass.getpass("Enter your password: ")
        if get_password(username) == password:
            print("Login successful! Welcome back, " + username + "!")
            show_menu()
        else:
            print("Invalid password. Please try again.")
            login()
    else:
        print("Username not found. Please register first.")
        welcome_message()

def view_order_history():
    global username
    clear_console()
    orders, total_bill = get_order_history(username)
    if orders:
        print("Here's your order history:")
        for i, (item, price) in enumerate(orders, start=1):
            print(f"\nOrder {i}:")
            print(f"{item} - ₱{price:.2f}")
        print(f"\nTotal Bill: ₱{total_bill:.2f}")
    else:
        print("You don't have any order history yet.")
    time.sleep(3)
    welcome_message()

def signup():
    clear_console()
    username = input("Choose a username: ")
    while username_exists(username):
        print("Username already exists. Please choose another one.")
        username = input("Choose a different username: ")
    password = getpass.getpass("Choose a password: ")
    confirm_password = getpass.getpass("Confirm password: ")
    while password != confirm_password:
        print("Passwords do not match. Please try again.")
        password = getpass.getpass("Choose a password: ")
        confirm_password = getpass.getpass("Confirm password: ")
    insert_user(username, password)
    print("Registration successful! You can now login.")
    time.sleep(2)
    welcome_message()

def show_menu():
    clear_console()
    time.sleep(1)
    print("")
    print("What tickles your taste buds today?")
    time.sleep(1)
    print("1: Food")
    print("2: Drinks or Liquid Happiness")
    while True:
        choice = input("Enter your choice (1 or 2): ")
        clear()
        if choice == '1':
            order_list = []  # Initialize order_list for food
            restaurant_foods(order_list)
            break
        elif choice == '2':
            show_drinks_menu([])
            break
        else:
            print("Whoopsie! That's not part of the list. Please choose 1 for Food or 2 for Drinks.")

def display_menu(menu, menu_name):
    print(f"\n{menu_name} Menu:")
    for number, item in menu.items():
        print(f"{number}: {item['name']} - ₱{item['price']:.2f}")

def restaurant_foods(order_list):
    while True:
        food_menu = {
            1: {"name": "Adobo", "price": 172.00},
            2: {"name": "Bulalo", "price": 181.00},
            3: {"name": "Kare-kare", "price": 499.99},
            4: {"name": "Lumpia Shanghai with sauce", "price": 500},
            5: {"name": "Sinigang Small", "price": 245.00},
            6: {"name": "Sinigang Medium", "price": 455.00},
            7: {"name": "Sinigang Large", "price": 755.00},
            8: {"name": "Spaghetti Single", "price": 70.00},
            9: {"name": "Spaghetti 3-5 persons", "price": 540.00},
            10: {"name": "Spaghetti 6-10 persons", "price": 750.00},
            11: {"name": "Spaghetti 11-15", "price": 850.00},
            12: {"name": "Tinola", "price": 112.38}
        }

        display_menu(food_menu, "EatEase Pinoy's Food")

        while True:
            request = input("\nPlease enter the number of your food choice and type 'done' if you're finished ordering: ")
            if request.lower() == 'done':
                clear()
                break

            if request.isdigit() and int(request) in food_menu:
                item = food_menu[int(request)]['name']
                price = food_menu[int(request)]['price']
                order_list.append((item, price))
                print(f"{item} is ready to rock your taste buds!")
            else:
                print(" ")
                print("Oops! That's not on our menu...")
                print(" ")
                time.sleep(1)
                print("It's not available. Please choose from the menu by entering the corresponding number.")
                print(" ")
                time.sleep(1)
                display_menu(food_menu, "EatEase Pinoy's Food")

        print("")

        drink_choice = input("Do you want to order some drinks? (yes/no): ")
        if drink_choice.lower() == 'yes':
            show_drinks_menu(order_list)
        elif drink_choice.lower() == 'no':
            clear()
            if order_list:
                total_bill = sum([order[1] for order in order_list])
                print("Here's your receipt:")
                for i, (item, price) in enumerate(order_list, start=1):
                    print(f"\nOrder {i}:")
                    print(f"{item} - ₱{price:.2f}")
                print(f"\nTotal Bill: ₱{total_bill:.2f}")
                # Pass both food and drinks order lists to payment
                payment(total_bill, order_list, 0, [])
                print("")
                print("Thanks for dining with us! Keep calm and munch on!")
                print()
                while True:
                    logout_choice = input("Would you like to logout? (yes/no): ")
                    print("")
                    if logout_choice.lower() == 'yes':
                        print("Thank you for choosing EatEase Pinoy Restaurant! Have a great day!")
                        sys.exit(0)
                    elif logout_choice.lower() == 'no':
                        print("What would you like to do next?")
                        show_menu()
                        return
                    else:
                        print("Invalid input. Please enter 'yes' or 'no'.")
                        clear_console()
                return
            else:
                print("Your order is empty. Please order something to proceed.")
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")
            clear_console()

def show_drinks_menu(order_list):
    clear_console()

    while True:
        drinks_menu = {
            1: {"name": "Coke", "price": 25.00},
            2: {"name": "7up", "price": 20.00},
            3: {"name": "Royal", "price": 25.00},
            4: {"name": "Sprite", "price": 25.00},
            5: {"name": "Water", "price": 0.00}
        }
        print("")

        display_menu(drinks_menu, "EatEase Pinoy's Drinks")
        print("")

        while True:
            request = input(" The number of your drink choice and type 'done' if you have finished ordering: ")
            if request.lower() == 'done':
                clear()
                clear_console()
                break
            if request.isdigit() and int(request) in drinks_menu:
                item = drinks_menu[int(request)]['name']
                price = drinks_menu[int(request)]['price']
                order_list.append((item, price))
                print("")
                print(f"{item} is ready to quench your thirst!")
                print("")
            else:
                print(" ")
                print("Oops! That's not on our drinks menu...")
                print(" ")
                time.sleep(1)
                print("It's not available buddy. Please choose from the soft drinks menu by entering the corresponding number.")
                print(" ")
                time.sleep(1)
                display_menu(drinks_menu, "EatEase Pinoy's Drinks")

        print("")

        order_food = input("Do you want to order food? (yes/no): ")
        clear_console()
        time.sleep(1)
        if order_food.lower() == 'yes':
            restaurant_foods(order_list)
        elif order_food.lower() == 'no':
            if order_list:
                total_bill = sum([order[1] for order in order_list])
                print("Here's your receipt:")
                for i, (item, price) in enumerate(order_list, start=1):
                    print(f"\nOrder {i}:")
                    print(f"{item} - ₱{price:.2f}")
                print(f"\nTotal Bill: ₱{total_bill:.2f}")
                # Pass both food and drinks order lists to payment
                payment(total_bill, order_list, 0, [])
                print("")
                print("Thanks for dining with us! Keep calm and munch on!")
                print()
                while True:
                    logout_choice = input("Would you like to logout? (yes/no): ")
                    print("")
                    if logout_choice.lower() == 'yes':
                        print("Thank you for choosing EatEase Pinoy Restaurant! Have a great day!")
                        sys.exit(0)
                    elif logout_choice.lower() == 'no':
                        print("What would you like to do next?")
                        show_menu()
                        return
                    else:
                        print("Invalid input. Please enter 'yes' or 'no'.")
                        clear_console()
                return
            else:
                print("Your order is empty. Please order something to proceed.")
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")
            clear_console()

# Modify the payment function to accept both food and drinks order lists
def payment(total_bill, order_list_food, total_drinks_bill, order_list_drinks):
    clear_console()
    print("Payment Process")
    print(f"Total Bill: ₱{total_bill:.2f}")
    print("\nHere are the items you've ordered:")
    
    for i, (item, price) in enumerate(order_list_food, start=1):
        print(f"\nOrder {i}:")
        print(f"{item} - ₱{price:.2f}")
    
    for i, (item, price) in enumerate(order_list_drinks, start=len(order_list_food) + 1):
        print(f"\nOrder {i}:")
        print(f"{item} - ₱{price:.2f}")

    while True:
        try:
            amount_paid = float(input("\nEnter the amount paid: ₱"))
            if amount_paid < total_bill:
                print("Insufficient amount paid. Please pay the total bill amount.")
            else:
                change = amount_paid - total_bill
                print(f"Change: ₱{change:.2f}")
                print("Thank you for your payment!")
                break
        except ValueError:
            print("Invalid input. Please enter a valid amount.")

create_table()
welcome_message()