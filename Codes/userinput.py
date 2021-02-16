import os
import time
import sys
from array import *
import string
import numpy as np

#number of elements/users in array.
size = 10   

#THIS WOULD BE THE "DATABASE"
users = ["uzi", "navid", "danny", "tamarr"]
pins = [2218, 1234, 4321, 0000]

class user:
    name = []
    pin = []
    i = 0


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
#check to see if the input is on the registered users list
#if they are, proceed to pin code. if not, try again 3 times before being kicked from module
    while (k < len(users)):
        if (currentName != users[k]):
            k += 1
            if (k == len(users)):
                print("Error. Unknown user. Wait", j, "seconds before attempting again.")
                time.sleep(j)
                currentName = input("Enter your username: ")
                k = 0
                j = j*2
                if (j > 30):
                    print("Too many failed attempts.")
                    exit()
        else:
            break

#user will have to enter the pin that matches the username they just entered
#if the pin is not integers the program will bug out so might need to fix this
#if the user enter the correct pin for their username, proceed to voice analysis
#if the user enters wrong pin, the program asks them to try again 3 more times
#with a delay in between each retry. After attempts > 4, program quits
    i = k
    j = 5
    #print("k and i are:", k, i)  
    currentPin = int(input("Enter your 4 digit PIN: "))
    while (currentPin != pins[i]):
        print("Error, pin is incorrect. Wait", j, "seconds before next attempt.")
        time.sleep(j)
        currentPin = int(input("Enter your PIN: "))
        j = j*2
        if (j > 30):
            print("Too many failed attempts.")
            exit()
    else:
        print("Success. Proceeding to voice analysis...\n")
        #NOW YOU WOULD GO TO VOICE ANALYSIS STUFF












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
