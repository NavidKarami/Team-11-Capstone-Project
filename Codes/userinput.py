import os
import time
import sys
from array import *
import string
import numpy as np

size = 5       #number of elements/users in array.

class user:
    name = []
    pin = []
    i = 0

def NewUser():

    print("New Pin")

    for i in range(size):
        user.pin.append("")

    while True:
        user.pin[user.i] = input("Choose your 4 digit pin: ")
        
        try:
            user.pin[user.i] = int(user.pin[user.i])
            print("You entered:", user.pin[user.i])
            NewUser_name()
            break

        except ValueError:
            print("You entered: ", user.pin[user.i])
            print("Integers allowed only. Try again.\n")

def NewUser_name():
    print("New UserName.")

    for j in range(size):
        user.name.append("")

    while True:
        user.name[user.i] = input("Choose a username; it must contains letters and numbers only: ")
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
    print("Welcome Current User.\n") 
    currentName = input("Enter your username: ")
    print("You entered: ", currentName)
    currentPin = int(input("Enter your PIN: "))
    print("You entered: ", currentPin)
    k = 0
    while (k < user.i):
        if (currentName == user.name[k] and currentPin == user.pin[k]):
            print("Match")
        k += 1

def userPrint():
    j = 0
    while (j < user.i):
        print("Your User Name is: %s and your PIN number is: %d" %(user.name[j], user.pin[j]))
        j += 1
        
def main():

    while True:
        print("1 for New user\n2 for current user\n3 for listing user info\n4 for terminating")
        select = input("What would you like to do: ")
        if (select == '1'):
            NewUser()
        elif (select == '2'):
            currentUser()
        elif (select == '3'):
            userPrint()
        elif (select == '4'):
            exit()
        else:
            print("Wrong input")

if __name__ == '__main__':
    main()