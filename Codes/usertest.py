import os
import time
import sys
from array import *
import string
import numpy as np
import re

class user:
    # There is a one-to-one relationship between the name and pin. name_index = pin_index for each user
    name = ["uzi", "navid", "danny", "tamarr"]
    pin = ['2218', '1000', '9999', '1234']
    i = 0
    len_name = len(name)  # length of the name array
    count = 0  # keeps track of user attempts entering pin
    trail = 0

# sets the amount of new users for database
size = user.i + 3


def NEWUSER():
    # New User Module
    # user creates their username. Program checks if their username already exists
    # no duplicate usernames are allowed

    while True:
        print("\nWelcome New User!")
        print("When entering your username, it contain numbers and letters.")
        print("Do not include any spaces! Do not enter a username being used.\n")
        name = input("Enter your username: ")
        #print(name) 
        check = bool(re.search(r"\s", name))
        #print(check)

        #Check the input string for spaces 
        if (check == True):
            print("\nThe username contains a space! Please try again.")
            continue
        else:
            print("\nThe username doesn't contain a space. Good job")
            
        if name in user.name:
            print("\nThe username is being used. Please try again")
        else:
            print("The username is not being used. Let's continue.\n")
            break

    # Stores the username in the system
    user.name.append(name)

    # Ask the user to create their four digit pin code
    # if something other than 4 numbers are entered must try again
    while True:
        print("As you enter your four-digit pincode ...")
        print("The length of the pincode needs to be four digits")
        print("The pincode can ONLY Contain Numbers") 
        #print("The pincode can Not be used by another user")
        pinnum = (input("Please enter your four-digit pincode: "))
        length = len(pinnum)
        if length != 4:  # checks length
            print("\nInvaild pincode, the length of the pincode is not four")
            print("Or the pincode is contained with characters") 
            print("Only enter numbers. Please try again!")
        elif pinnum.isdigit() == False:  # checks if they entered something other than numbers for their pin
            print("\nInvaild pincode, the length of the pincode is not four")
            print("Or the pincode is contained with characters")
            print("Only enter numbers. Please try again.")
        else:
            break

    # confirm the pin
    while True:
        pinnum2 = (input("\nPlease confirm your pin: "))
        length2 = len(pinnum2)
        # Confirm the four-digit pincode (Compare)
        if (pinnum != pinnum2):
            print("\nThe pin does not match. Try again.")
        else:
            break

            # Store the pincode in the system
    user.pin.append(pinnum)


# what is this stuff below? do we need it or can we delete it?#################
def currentUser():
    #print(user.name)
    length_name = len(user.name)
    '''
    print("Length in the list: ",length_name) 
    print("Length origin: ", user.len_name)
    '''
    print("Welcome Current User.\n") 
    temp_name = input("Enter your username: ")
    k = 0

    #loop until you find the name
    for k in range(0, length_name):
        #print(user.name[k])
        if(temp_name == user.name[k]):
            print("Welcome: ", temp_name)
            index = k
            name = temp_name
            current_user_pin(name, index) #go to check the current user pin
    #didn't find the name. ask the user re-enter name
    print("Invalid user name. Try again.")
    user.trail = user.trail + 1 
    if (user.trail == 3):
        print("Too many attempts. Locking you out for 10 sec.")
        time.sleep(10)
        main()
    currentUser()
    


# this code is used to determine the user based on the pin they enter
def current_user_pin(name,index):


    user.len_name = len(user.pin)
    temp_pin = input("\nEnter your pin:")
    # checks the pin to find a match. If there's a match, username associated to
    # that pin is displayed. Then we proceed to voice analysis
    for k in range(0, user.len_name):
        if (str(temp_pin) == str(user.pin[k])):
            print("Welcome: ", user.name[k])
            user.count = 0
            print("We go to FFT from here.")
            main() #would go to fft module not main###########

    # if the input doesn't match any of the pins from the pin array...
    print("Invalid. Try again.")
    user.count = user.count + 1  # inc and check to see if they atmp three times
    if (user.count == 3):
        print("Too many attempts. Locking you out for 10 sec.")
        time.sleep(10)  # sleep
        main()  # do we want to go to main or just have them restart pin attempts?##########
    current_user_pin(name,index)  # call the pin function again


# It prints out the current user info. Not sure what data we want to print
# but as of rn it prints users and pins

def userPrint():
    # testing################################################
    z = 0
    k = 0
    x = len(user.name)
    y = len(user.pin)
    print("\nRegistered users: ")
    while (z < x):
        print(user.name[z])
        z += 1
    print("\nPins:")
    while (k < y):
        print(user.pin[k])
        k += 1


def main():
    print("\nWELCOME!")
    # this is the main menu for our program. there are various options to choose from
    # any number that isn't a valid option will get an error message. Program runs till
    # the user terminates it
    while True:
        print("\n[1]: New user\n[2]: Current user\n[3]: TESTING PHASE (View User Info)\n[4]: Exit")
        select = input("Please select from the options above: ")
        if (select == '1'):
            NEWUSER()
        elif (select == '2'):
            currentUser()
        elif (select == '3'):
            userPrint()
        elif (select == '4'):
            exit()
        else:
            print("\nError. Invalid input. Try again.")


if __name__ == '__main__':
    main()
