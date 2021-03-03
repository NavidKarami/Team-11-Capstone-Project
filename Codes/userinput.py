import os
import time
import sys
from array import *
import string
import numpy as np  

class user:
    #There is a one-to-one relationship between the name and pin. name_index = pin_index for each user
    name = ["uzi", "navid", "danny", "tamarr"]
    pin = ['2218', '1000', '9999', '1234']
    i = 0 
    len_name = len(name)  #Len of the name array
    count = 0 #keeps track of user attempts entering pin
    
#sets the amount of registered users for database
size = user.i + 3

def NEWUSER():
    #New User Module 
    #Ask the user to type the name
    while True:
        print("Since you are new into our system")
        name = input("Enter your name\n")
        quit = True 
        for un in user.name:
            if(name == un):
                print("There is aleaday a username in the list")
                print("Please input your name again")
                quit = False
                break
        if(quit):
            break

    #Store the username in the system 
    user.name.append(name)
    print(user.name)

    #Ask the user for a four digit pin code 
    #if the four-digit wasn't entered properly, Ask the user agian 
    while True:
        #check the length and numbers only 
        pinnum = (input("Please enter your four-digit pincode\n"))
        #print(pinnum)
        length = len(pinnum)
        print(length)
        # Known: won't if you put in and 0000 within the pincode
        if length !=4 or pinnum in user.pin:
        #if(length != 4):
            print("Invaild pincode, please try again!")
            print("The pincode is being used")
        else:            
           break

    print("This is the pincode: ", pinnum)
    #print(pinnum)
    
    while True:
        #Check if we have the same pincode 
        print("It's time to confirm your pincode")
        pinnum2 = (input("Please enter your four-digit pincode\n"))
        #print(pinnum2)
        length2 = len(pinnum2)
        #Confirm the four-digit pincode (Compare) 
        if(pinnum != pinnum2):
            print("The confirm pincode does not matched please try again")
        else:
            break 

    #Store the pincode in the system
    user.pin.append(pinnum)
    print(user.pin)
    
'''
* To check if an item is in a list, the "in" operator can be used 
* The in operator is alos used to determine whether or not a string is a substring of another string 
'''

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
    user.len_name = len(user.pin)
    print("checking:", user.len_name)
    temp_pin = input("Enter your pin:")
    #check the pin to match index. check name. Double checking is good
    for k in range(0, user.len_name):
        if(str(temp_pin) == str(user.pin[k])):
            print("Welcome: ", user.name[k])
            user.count = 0
            print("We go to FFT from here.")
            #exit(0)
            main() #It

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
            NEWUSER()
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
