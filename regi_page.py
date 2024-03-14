from lms import *


'''Fuction which is used to get the choice from the user'''


def choices():
    print("Please choose what you would like to do.")
    choice = int(input("1 For Registration and 2 For Login: "))
    if choice == 1:
       return getdetails()
    elif choice == 2:
       return checkdetails()
    else:
        print("Invalid option")
        return choices()


'''Fuction which is used to get the details from the user'''


def getdetails():
    print("Please Provide")
    name = str(input("Username: "))
    email_id = str(input("Email ID: "))
    mobile_no=[]
    mobile_no = input("Mobile No: ")
    if(len(mobile_no)==10):
        pass
    else:
        print("Mobile Number is invalid!!!")
        return getdetails()
    password = str(input("Password: "))
    confirm_password = str(input("Confirm Password: "))
    f = open("User_Data.txt",'r')
    info = f.read()
    if name in info:
        print("Username already taken.Please Try Again")
        return getdetails()
    f.close()
    if (password==confirm_password):
        f = open("User_Data.txt",'a')
        info =name + "  " + password
        f.writelines(info+"\n")
        f.close()
        print("Sucessfully Registered")
        checkdetails()
    else:
        print("Password does not match")
        return getdetails()



'''Fuction which is used to verify the login details from the user'''

def checkdetails():
    print("Please Login")
    name = input("Username: ")
    password = str(input("Password: "))
    f = open("User_Data.txt",'r')
    info = f.read()
    info = info.split()
    if name in info:
        index = info.index(name) + 1
        usr_password = info[index]
         
        if usr_password==password:
            print("Welcome Back, " + name)
            start_project()
        else:
            print("Password entered is wrong")
            return checkdetails()
    else:
        print("Name not found. Please Sign Up.")
        return choices()
    
choices()
