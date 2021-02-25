import os
import time
import sys
from array import *
import string
import numpy as np  

###########################################
#fix the pins, allow 000x because it doesn't right now

class user:
    #There is a one-to-one relationship between the name and pin. name_index = pin_index for each user
    name = ["uzi", "navid", "danny", "tamarr"]
    pin = [2218, 1000, 9999, 1234]
    i = len(name) 
    len_name = len(name)  #Len of the name array
    count = 0 #keeps track of user attempts entering pin
    
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

#We do not need this at this time. The program only checks for the pin. No username comparison needed for current users
"""
def currentUser():
    print("Welcome Current User.\n") 
    temp_name = input("Enter your username: ")
    k = 0
    #loop until you find the name
    for k in range(0, user.len_name):
        if(temp_name == user.name[k]):
            print("Welcome: ", temp_name)
            index = k
            name = temp_name
            current_user_pin(name, index) #go to check the current user pin
    #didn't find the name. ask the user re-enter name
    print("Invalid user name. Try again.")
    currentUser()
"""

#def current_user_pin(name, index):
def current_user_pin():
    temp_pin = input("Enter your pin:")
    #check the pin to match index. check name. Double checking is good
    for k in range(0, user.len_name):
        if(str(temp_pin) == str(user.pin[k])):
            print("Welcome: ", user.name[k])
            user.count = 0
            print("We go to FFT from here.")
            exit(0)

    print("invalid. Try again.")
    user.count = user.count + 1 #inc and check to see if they atmp three times
    if(user.count == 3):
        print("Too many attempts. Locking you out for 10 sec")
        time.sleep(10) #sleep
        main()
    current_user_pin() #call the pin function again

#It prints out the current user info. It is a test module. Not working at this time
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
#########################################################
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
            current_user_pin()
        elif (select == '3'):
            userPrint()
        elif (select == '4'):
            exit()
        else:
            print("\nError. Invalid input. Try again.")

if __name__ == '__main__':
    main()
