import os
import time
import sys
from array import *
import string
import numpy as np  

###########################################
#fix the pins, allow 000x because it doesn't right now

class user:
    name = ["uzi", "navid", "danny", "tamarr"]
    pin = [2218, 1000, 9999, 1234]
    i = len(name)
    
#sets the amount of registered users for database
size = user.i + 3


def NewUser():
#this append might be wrong im not sure
    if (user.i < size):
        user.pin.append("")
        
#following code asks user to create a 4 digit pin, save as a string
        while True:
            user.pin[user.i] = input("\nSet your 4 digit pin: ")
            x = str(user.pin[user.i])
            #print("\nYou entered:", user.pin[user.i])
        
#checks if the pin is 4 integers long, if it is then you create a username  
            if (len(x) == 4) and (x.isdigit()):
                NewUser_name()
                break
#if it isn't you must keep trying until you meet the requirements
            else:
                print("Error. Try again.")
    else:
        print("can't register new users")


def NewUser_name():
#append is wrong not sure why
#need to check that username doesn't match an already active username#########
    user.name.append("")
    user.name[user.i] = input("Choose a username. Must contains letters and numbers only: ")

#not sure what the code below is for...###################################
    if (user.name[user.i].isdigit()):
        raise ValueError("The user name must contain letters and numbers.")
        user.name[user.i] = str(user.name[user.i])
        user.i += 1
########################################################################

#to increment the array so we don't overwrite any users
    user.i += 1


def currentUser():
#asks user to enter their name and pin
    print("\nWelcome Back!")
    username = input("Enter your username: ")
    k = 0
#check to see if the entered username is on the registered users list
#if they are, proceed to pin code. if not, keep trying until a valid username is entered
    while (k < len(user.name)):
        if (username != user.name[k]):
            k += 1
            if (k == len(user.name)):
                print("Error. Unknown user. Please enter valid username.")
                username = input("Enter your username: ")
                k = 0   #to reset the array so we start at the 1st element
        else:
            break

#user will have to enter pin that matches the username they just entered

##########################################################
        #if the pin is not integers the program will bug out so might need to fix this

#if the user enters the correct pin for their username, proceed to voice analysis
#if the user enters wrong pin, the program asks them to try again 3 more times
#if failed attempts > 3, delay for 10 minutes then reset the attempt count
    i = k   #to ensure we match the correct user/pin from each array
    j = 0
    print("k and i are:", k, i)  
    userpin = int(input("Enter your 4 digit PIN: "))
    
##################################################################
#fix the below, make sure user enters 4 digits or else they can't proceed
    #while (len(currentPin) != 4):


#########SOMETHING IS WRONG BELOW WTF IDK WHAT
    x = len(user.name)
    y = len(user.pin)
    z = user.i
    print("various checks\n length of arrays:",x, y, "\ncount of users:", z)
    print("check:", userpin, user.pin[i])
    
    if (userpin == user.pin[i]):
        print("good\n")
    
    
    while (userpin != user.pin[i]):
        print("Error, pin is incorrect. Please try again.")
        userpin = int(input("Enter your PIN: "))
        j += 1
        if (j > 2):
            time.sleep(10)
            j = 0   #to reset the attempt count
            print("restart")
    else:
        print("Success. Proceeding to voice analysis...\n")
        #NOW YOU WOULD GO TO VOICE ANALYSIS STUFF












#not sure what this code below does
def userPrint():
#testing################################################
    z = 0
    k = 0
    x = len(user.name)
    y = len(user.pin)
    print("check lenght of arrays:", x, y)

    while (z < x):
        print("users:", user.name[z])
        z += 1

    while (k < y):
        print("pins:", user.pin[k])
        k += 1
######################################################################
    #j = 0
    #while (j < user.i):
        #print("Your User Name is: %s and your PIN number is: %d" %(user.name[j], user.pin[j]))
        #j += 1




       
def main():

    print("\nWELCOME!\n")
    #this is the main menu for our program. there are various options to choose from
    #any number that isn't a valid option will get an error message. Program runs till
    #the user terminates it
    while True:
        print("[1]: New user\n[2]: Current user\n[3]: TESTING PHASE (View User Info)\n[4]: Exit")
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
