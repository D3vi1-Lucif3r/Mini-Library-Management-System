'''library management system'''

from datetime import date
from datetime import timedelta
import os
os.getcwd()
    

class LMS:


    '''Constructor-It is used to intialise values for certain variable'''
    def __init__(self, list_of_books, library_name):
        self.list_of_books = "list_of_books.txt"
        self.library_name = library_name
        self.books_dict = {}
        id = 101
        with open(self.list_of_books) as b:
            content = b.readlines()
        for line in content:
            self.books_dict.update({str(id):{'books_title':line.replace("\n",""),'lender_name':'','lend_date':'', 'status':'Available'}})
            id += 1



    '''Fuction to display the books'''


    def display_books(self):
        print("------------------------List of Books---------------------")
        print("Books ID","\t", "Title")
        print("----------------------------------------------------------")
        for key, value in self.books_dict.items():
            print(key,"\t\t", value.get("books_title"), "- [", value.get("status"),"]")



    '''Fuction to issue books'''


    def Issue_books(self):
        books_id = input("Enter Books ID : ")
        current_date=date.today()
        return_date=current_date+timedelta(days=7)
        if books_id in self.books_dict.keys():
            if not self.books_dict[books_id]['status'] == 'Available':
                print(f"This book is already issued to {self.books_dict[books_id]['lender_name']} on {self.books_dict[books_id]['lend_date']}")
                return self.Issue_books()
            elif self.books_dict[books_id]['status'] == 'Available':
                your_name = input("Enter Your Name : ")
                self.books_dict[books_id]['lender_name'] = your_name
                self.books_dict[books_id]['lend_date'] = current_date
                self.books_dict[books_id]['status']= 'Already Issued'
                self.books_dict[books_id]['last_date']=return_date
                print(f"Book Issued Successfully on {self.books_dict[books_id]['lend_date']} to {self.books_dict[books_id]['lender_name']}!!!\n")
                print(f"Please Return The Book On Or Before {self.books_dict[books_id]['last_date']}!!!\n")
        else:
            print("Book ID Not Found !!!")
            return self.Issue_books()


    '''Fuction to add books to the library'''


    def add_books(self):
        new_books = input("Enter Books Title : ")
        if new_books == "":
            return self.add_books()
        elif len(new_books) > 20:
            print("Books title length is too long !!! Title length limit is 20 characters")
            return self.add_books()
        else:
            with open(self.list_of_books, "a") as b:
                b.writelines(f"{new_books}\n")
            self.books_dict.update({str(int(max(self.books_dict))+1):{'books_title':new_books,'lender_name':'','lend_date':'', 'status':'Available'}})
            print(f"The books '{new_books}' has been added successfully !!!")



    '''Function to return books'''
    def return_books(self):
        books_id = input("Enter Books ID : ")
        current_date=date.today()
        return_date=current_date+timedelta(days=7)
        if books_id in self.books_dict.keys():
            if self.books_dict[books_id]['status'] == 'Available':
                print("This book is already available in library. Please check book id. !!! ")
                return self.return_books()
            elif not self.books_dict[books_id]['status'] == 'Available':
                your_name = input("Enter Your Name : ")
                self.books_dict[books_id]['lender_name'] = your_name
                self.books_dict[books_id]['lend_date'] = current_date
                self.books_dict[books_id]['status']= 'Available'
                print(f"Book Successfully Returned by {self.books_dict[books_id]['lender_name']} On {self.books_dict[books_id]['lend_date']}!!!\n")
        else:
            print("Book ID Not Found !!!")


'''Main function which is used to call all the other function'''
def start_project():
    
        mylms = LMS("list_of_books.txt", "Python's")
        press_key_list = {"D": "Display Books", "I": "Issue Books", "A": "Add Books", "R": "Return Books", "Q": "Quit"}    
        
        key_press = False
        while not (key_press == "q"):
            print(f"\n----------Welcome To {mylms.library_name}'s Library Management System---------\n")
            for key, value in press_key_list.items():
                print("Press", key, "To", value)
            key_press = input("Press Key : ").lower()
            if key_press == "i":
                print("\nCurrent Selection : ISSUE BOOK\n")
                mylms.Issue_books()
                
            elif key_press == "a":
                print("\nCurrent Selection : ADD BOOK\n")
                mylms.add_books()

            elif key_press == "d":
                print("\nCurrent Selection : DISPLAY BOOKS\n")
                mylms.display_books()
            
            elif key_press == "r":
                print("\nCurrent Selection : RETURN BOOK\n")
                mylms.return_books()
            elif key_press == "q":
                break
            else:
                print("Invalid Selection!!!\n")
                return start_project()
