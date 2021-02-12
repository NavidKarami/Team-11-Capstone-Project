import os
import time
import sys
from array import *
import string
import numpy as np

#number of elements/users in array.
size = 10   

class user:
    name = []
    pin = []
    i = 0

#THIS WOULD BE THE "DATABASE"
users = ["uzi", "navid", "danny", "tamarr"]
pins = [2218, 1234, 4321, 0000]


def NewUser():
#not sure what this code below does...(following two lines)
    for i in range(size):
        user.pin.append("")

#following code asks user to create a 4 digit pin
    while True:
        user.pin[user.i] = input("\nSet your 4 digit pin: ")
        x = str(user.pin[user.i])
#print("\nYou entered:", x)
#checks if the pin is 4 integers long, if it is then you create a username  
        if (len(x) == 4) and (x.isdigit()):
                NewUser_name()
                break
#if it isn't you must keep trying until you meet the requirements
        else:
                print("Error. Try again.")

def NewUser_name():
#again, not sure what this does...    
    for j in range(size):
        user.name.append("")

    while True:
        user.name[user.i] = input("Choose a username. Must contains letters and numbers only: ")
        try:
            if (user.name[user.i].isdigit()):
                raise ValueError("The user name must contain letters and numbers.")

            user.name[user.i] = str(user.name[user.i])
            print("You entered:", user.name[user.i])
            user.i += 1 
            print("i is:", user.i)
            break

        except ValueError:
            print("You entered: ", user.name[user.i])
            print("characters and numbers allowed only. Try again.\n")
   

def currentUser():
#asks user to enter their name and pin
    print("\nWelcome Back!") 
    currentName = input("Enter your username: ")
    k = 0
    j = 5
    while (k < len(users)):
        if (currentName != users[k]):
            k += 1
            if (k == len(users)):
                print("Error. Unknown user.\n")
                time.sleep(j)
                currentName = input("Enter your username: ")
                k = 0
                print("delay j is:", j)
                j = j*3
            #print("step\n")
        else:
            break

    #if (k == len(users)):
     #   print("Error. Unknown user.\n")
        
            #j = k
            #currentPin = int(input("Enter your PIN: "))
            #if (currentPin != pins[j]):
            #    print("good")






#check to see if the user input matches with database info
#this matching needs to be reworked to compare with the "database"

    #testing down BELOW
    #r = len(users)
    #print("this is r:", r)

    #currentPin != pins[k]

#not sure what this code below does, isn't called anywhere in the code
def userPrint():
    j = 0
    while (j < user.i):
        print("Your User Name is: %s and your PIN number is: %d" %(user.name[j], user.pin[j]))
        j += 1
        
def main():

    print("\nWELCOME!\n")
    #this is the main menu for our program. there are various options to choose from
    #any number that isn't a valid option will get an error message. Program runs till
    #the user terminates it
    while True:
        print("[1]: New user\n[2]: Current user\n[3]: View user info\n[4]: Exit")
        select = input("Please select from the options above: ")
        if (select == '1'):
            NewUser()
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
