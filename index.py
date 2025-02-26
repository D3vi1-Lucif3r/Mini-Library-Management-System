import json
import os
from datetime import datetime, timedelta
import logging

# Set up logging
logging.basicConfig(filename='library_system.log', level=logging.ERROR)

# File paths
BOOK_INVENTORY_FILE = "book_inventory.json"
LOAN_HISTORY_FILE = "loan_history.json"
MEMBER_PROFILES_FILE = "member_profiles.json"
RESERVATIONS_FILE = "reservations.json"
USER_LOANS_FILE = "user_loans.json"

# Constants
BORROW_PERIOD_DAYS = 14
OVERDUE_FINE_PER_DAY = 5

# Utility functions for loading and saving data
def load_data(file_path):
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                return json.load(file)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {file_path}")
    return {}

def save_data(file_path, data):
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
    except IOError as e:
        logging.error(f"IO error occurred when writing to {file_path}: {e}")
        print(f"Error saving data. Please try again.")

# Initializing
book_inventory = load_data(BOOK_INVENTORY_FILE)
loan_history = load_data(LOAN_HISTORY_FILE)
member_profiles = load_data(MEMBER_PROFILES_FILE)
reservations = load_data(RESERVATIONS_FILE)
user_loans = load_data(USER_LOANS_FILE)

# Default user profiles (To handle no users)
if not member_profiles:
    member_profiles = {}
    save_data(MEMBER_PROFILES_FILE, member_profiles)

# User registration function
def create_user_account():
    while True:
        try:
            username = input("Enter a username to register: ")
            if not username:
                raise ValueError("Username cannot be empty.")
            if username in member_profiles:
                print("Username already exists.")
                continue

            password = input("Enter a password: ")
            if not password:
                raise ValueError("Password cannot be empty.")

            role = input("Enter user role (admin or user): ").lower()
            if role not in ['admin', 'user']:
                raise ValueError("Invalid role. Please enter either 'admin' or 'user'.")

            member_profiles[username] = {"password": password, "role": role}
            save_data(MEMBER_PROFILES_FILE, member_profiles)
            print(f"Registration successful for '{username}'.")
            break
        except ValueError as ve:
            print(f"Error: {ve}")

# User login function
def authenticate_user():
    while True:
        try:
            print("\n1. Login")
            print("2. Register")
            choice = input("Enter your choice (1 for Login, 2 for Register): ")

            if choice == '1':
                username = input("Enter username: ")
                password = input("Enter password: ")

                if username in member_profiles and member_profiles[username]["password"] == password:
                    print(f"Login successful! Welcome, {username}.")
                    return username, member_profiles[username]["role"]
                else:
                    raise ValueError("Invalid username or password.")
            elif choice == '2':
                create_user_account()
            else:
                print("Invalid choice. Please select either 1 or 2.")
        except ValueError as ve:
            print(f"Error: Please enter a value.")

# Add new book function with admin restriction
def add_new_book(role):
    if role != "admin":
        print("Unauthorized access. Only admins can add books.")
        return

    try:
        book_title = input("Enter the book title: ")
        if not book_title:
            raise ValueError("Book title cannot be empty.")
        if book_title in book_inventory:
            print(f"'{book_title}' already exists in the library.")
            return

        author = input("Enter the author's name: ")
        genre = input("Enter the genre: ")
        year = input("Enter the publication year: ")

        book_inventory[book_title] = {
            "author": author,
            "genre": genre,
            "year": year,
            "availability": "available"
        }
        save_data(BOOK_INVENTORY_FILE, book_inventory)
        print(f"'{book_title}' by {author} added to the library.")
    except ValueError as ve:
        print(f"Error: Please enter a value.")

# View available books
def view_books():
    print("\nAvailable Books:")
    if not book_inventory:
        print("There are no books in the library. Wait for the books to be added.")
    else:
        for book, details in book_inventory.items():
            print(f"- {book} by {details['author']} (Genre: {details['genre']}, Year: {details['year']}, Availability: {details['availability']})")
    print("\n")

# Search for books by keyword (title, author, or genre)
def search_books():
    search_term = input("Enter a keyword to search (title, author, or genre): ").lower()
    found_books = [book for book, details in book_inventory.items() if search_term in book.lower() or search_term in details['author'].lower() or search_term in details['genre'].lower()]

    if found_books:
        print("\nSearch Results:")
        for book in found_books:
            details = book_inventory[book]
            print(f"- {book} by {details['author']} (Genre: {details['genre']}, Year: {details['year']}, Availability: {details['availability']})")
    else:
        print(f"No books found matching '{search_term}'.\n")

# Borrow book with borrowing limit check and availability
def borrow_library_book(username):
    if username not in user_loans:
        user_loans[username] = []

    if len(user_loans[username]) >= 3:  # Borrow limit
        print("Borrow limit reached. Please return a book before borrowing another.")
        return

    try:
        view_books()
        book_title = input("Enter the title of the book to borrow: ")
        if not book_title:
            raise ValueError("Book title cannot be empty.")
        if book_title in book_inventory and book_inventory[book_title]["availability"] == "available":
            book_inventory[book_title]["availability"] = "borrowed"
            loan_history[book_title] = {"borrower": username, "borrow_date": datetime.now().strftime("%Y-%m-%d")}
            user_loans[username].append(book_title)
            save_data(BOOK_INVENTORY_FILE, book_inventory)
            save_data(LOAN_HISTORY_FILE, loan_history)
            save_data(USER_LOANS_FILE, user_loans)
            print(f"'{book_title}' has been borrowed by {username}.")
        else:
            print(f"'{book_title}' is not available for borrowing.")
    except ValueError as ve:
        print(f"Error: {ve}")

# Return book
def return_library_book(username):
    try:
        book_title = input("Enter the title of the book to return: ")
        if not book_title:
            raise ValueError("Book title cannot be empty.")
        if book_title in loan_history and loan_history[book_title]["borrower"] == username:
            borrow_date = loan_history[book_title]["borrow_date"]
            fine = calculate_fine(borrow_date)

            book_inventory[book_title]["availability"] = "available"
            del loan_history[book_title]
            user_loans[username].remove(book_title)
            save_data(BOOK_INVENTORY_FILE, book_inventory)
            save_data(LOAN_HISTORY_FILE, loan_history)
            save_data(USER_LOANS_FILE, user_loans)

            if book_title in reservations and reservations[book_title]:
                reserved_user = reservations[book_title].pop(0)
                print(f"'{book_title}' has been returned. Notifying {reserved_user}.")
                if not reservations[book_title]:
                    del reservations[book_title]
                save_data(RESERVATIONS_FILE, reservations)
            print(f"'{book_title}' has been returned by {username}. Fine: ₹{fine}.")
        else:
            print(f"'{book_title}' is either not borrowed by you or does not exist.")
    except ValueError as ve:
        print(f"Error: {ve}")

# Calculate fine
def calculate_fine(borrow_date):
    return_date = datetime.now()
    due_date = datetime.strptime(borrow_date, "%Y-%m-%d") + timedelta(days=BORROW_PERIOD_DAYS)
    
    if return_date > due_date:
        overdue_days = (return_date - due_date).days
        fine = overdue_days * OVERDUE_FINE_PER_DAY
        return fine
    return 0

# Reserve a book
def reserve_book(username):
    try:
        book_title = input("Enter the title of the book to reserve: ")
        if book_title in book_inventory:
            if book_inventory[book_title]["availability"] == "borrowed":
                if book_title not in reservations:
                    reservations[book_title] = []
                reservations[book_title].append(username)
                save_data(RESERVATIONS_FILE, reservations)
                print(f"You have reserved the book '{book_title}'.")
            else:
                print(f"'{book_title}' is available. You can borrow it instead of reserving.")
        else:
            print(f"'{book_title}' is not found in the library.")
    except ValueError as ve:
        print(f"Error: {ve}")

# Main menu to interact with the system
def main_menu():
    username, role = authenticate_user()

    while True:
        print("\n===== Library Menu =====")
        print("1. View Books")
        print("2. Search Books")
        print("3. Borrow Book")
        print("4. Return Book")
        print("5. Reserve Book")
        print("6. Add New Book(Only for Admin.)")
        print("7. Exit")

        choice = input("Enter your choice: ")
        if choice == '1':
            view_books()
        elif choice == '2':
            search_books()
        elif choice == '3':
            borrow_library_book(username)
        elif choice == '4':
            return_library_book(username)
        elif choice == '5':
            reserve_book(username)
        elif choice == '6' and role == "admin":
            add_new_book(role)
        elif choice == '7':
            print("Exiting the library system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
